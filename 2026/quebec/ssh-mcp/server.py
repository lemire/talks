#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]>=1.2.0",
#     "paramiko>=3.4.0",
# ]
# ///
"""MCP server exposing sandboxed SSH/SFTP file operations.

Configuration is read from credentials.json sitting next to this script.
All tool paths are resolved relative to (and confined within) the
`remotedirectory` named in that file — attempts to escape it are rejected.
"""

from __future__ import annotations

import json
import os
import posixpath
import stat
from pathlib import Path
from typing import Any

import paramiko  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from mcp.server.fastmcp import FastMCP  # pyright: ignore[reportMissingImports, reportMissingModuleSource]

CREDENTIALS_PATH = Path(__file__).resolve().parent / "credentials.json"


def _load_credentials() -> dict[str, Any]:
    if not CREDENTIALS_PATH.is_file():
        raise RuntimeError(f"credentials.json not found at {CREDENTIALS_PATH}")
    with CREDENTIALS_PATH.open("r", encoding="utf-8") as f:
        creds = json.load(f)
    for required in ("host", "username", "remotedirectory"):
        if not creds.get(required):
            raise RuntimeError(f"credentials.json is missing '{required}'")
    return creds


CREDS = _load_credentials()
SANDBOX_ROOT = posixpath.normpath(CREDS["remotedirectory"])
if not posixpath.isabs(SANDBOX_ROOT):
    raise RuntimeError("'remotedirectory' must be an absolute path")

mcp = FastMCP("ssh-files")


def _resolve(user_path: str) -> str:
    """Resolve a tool-supplied path against the sandbox.

    Relative paths are joined onto SANDBOX_ROOT. Absolute paths are accepted
    only if they already lie inside SANDBOX_ROOT. Any path that normalises
    outside the sandbox is rejected.
    """
    if user_path in ("", "."):
        return SANDBOX_ROOT
    if posixpath.isabs(user_path):
        candidate = posixpath.normpath(user_path)
    else:
        candidate = posixpath.normpath(posixpath.join(SANDBOX_ROOT, user_path))
    if candidate != SANDBOX_ROOT and not candidate.startswith(SANDBOX_ROOT + "/"):
        raise PermissionError(
            f"Path '{user_path}' is outside the allowed remote directory"
        )
    return candidate


class _Session:
    """Context manager that opens an SFTP session and tears it down cleanly."""

    def __enter__(self) -> paramiko.SFTPClient:
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()

        known_hosts = CREDS.get("known_hosts")
        if known_hosts:
            self._ssh.load_host_keys(os.path.expanduser(known_hosts))
        if CREDS.get("strict_host_key_checking", True):
            self._ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        else:
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key_path = CREDS.get("key_path")
        password = CREDS.get("password")
        passphrase = CREDS.get("passphrase")

        connect_kwargs: dict[str, Any] = {
            "hostname": CREDS["host"],
            "port": int(CREDS.get("port", 22)),
            "username": CREDS["username"],
            "allow_agent": True,
            "look_for_keys": key_path is None and password is None,
        }
        if key_path:
            connect_kwargs["key_filename"] = os.path.expanduser(key_path)
        if password:
            connect_kwargs["password"] = password
        if passphrase:
            connect_kwargs["passphrase"] = passphrase

        self._ssh.connect(**connect_kwargs)
        self._sftp = self._ssh.open_sftp()
        return self._sftp

    def __exit__(self, *exc_info: object) -> None:
        del exc_info  # not used; we always close both handles
        try:
            self._sftp.close()
        finally:
            self._ssh.close()


@mcp.tool()
def sandbox_info() -> dict[str, Any]:
    """Return the remote sandbox root and connection target.

    All other tools confine their operations to this directory.
    """
    return {
        "remote_directory": SANDBOX_ROOT,
        "host": CREDS["host"],
        "port": int(CREDS.get("port", 22)),
        "username": CREDS["username"],
    }


@mcp.tool()
def upload_file(local_path: str, remote_path: str, overwrite: bool = True) -> str:
    """Upload a local file into the sandboxed remote directory via SFTP.

    Args:
        local_path: Path to the local file to upload.
        remote_path: Destination path relative to the sandbox (or an
            absolute path that lies inside it).
        overwrite: If False, fail when the remote path already exists.
    """
    local = Path(local_path).expanduser()
    if not local.is_file():
        raise FileNotFoundError(f"Local file does not exist: {local}")
    target = _resolve(remote_path)
    with _Session() as sftp:
        if not overwrite:
            try:
                sftp.stat(target)
            except FileNotFoundError:
                pass
            else:
                raise FileExistsError(f"Remote path already exists: {target}")
        sftp.put(str(local), target)
        size = sftp.stat(target).st_size
    return f"Uploaded {local} -> {target} ({size} bytes)"


def _ensure_remote_dir(sftp: paramiko.SFTPClient, target_dir: str, seen: set[str]) -> None:
    """Create target_dir (and missing parents) inside the sandbox, once.

    `seen` caches directories already known to exist for this session so a
    batch of files sharing parents does not re-stat the same paths repeatedly.
    """
    if target_dir in seen or target_dir == SANDBOX_ROOT:
        seen.add(target_dir)
        return
    parts = target_dir[len(SANDBOX_ROOT) + 1 :].split("/")
    current = SANDBOX_ROOT
    for part in parts:
        if not part:
            continue
        current = posixpath.join(current, part)
        if current in seen:
            continue
        try:
            sftp.stat(current)
        except FileNotFoundError:
            sftp.mkdir(current)
        seen.add(current)


@mcp.tool()
def upload_files(
    files: list[dict[str, str]],
    overwrite: bool = True,
    make_parents: bool = True,
) -> dict[str, Any]:
    """Upload many files (hundreds) over a single reused SSH/SFTP session.

    This is far faster than calling upload_file repeatedly, which reconnects
    for every file. All transfers share one connection.

    Args:
        files: List of {"local_path": ..., "remote_path": ...} mappings. Each
            remote_path is relative to the sandbox (or an absolute path inside
            it). Paths are resolved and confined to the sandbox.
        overwrite: If False, existing remote files are skipped (not an error).
        make_parents: If True, create any missing parent directories.

    Returns:
        A summary with per-file results: counts of uploaded/skipped/failed and
        a list of any failures with their error messages.
    """
    if not files:
        return {"uploaded": 0, "skipped": 0, "failed": 0, "failures": [], "total": 0}

    # Validate and resolve everything up front so a bad entry fails fast,
    # before we open the connection.
    resolved: list[tuple[Path, str]] = []
    for i, entry in enumerate(files):
        local_raw = entry.get("local_path")
        remote_raw = entry.get("remote_path")
        if not local_raw or not remote_raw:
            raise ValueError(
                f"files[{i}] must have both 'local_path' and 'remote_path'"
            )
        local = Path(local_raw).expanduser()
        if not local.is_file():
            raise FileNotFoundError(f"Local file does not exist: {local}")
        resolved.append((local, _resolve(remote_raw)))

    uploaded = 0
    skipped = 0
    failures: list[dict[str, str]] = []
    seen_dirs: set[str] = set()

    with _Session() as sftp:
        for local, target in resolved:
            try:
                if not overwrite:
                    try:
                        sftp.stat(target)
                    except FileNotFoundError:
                        pass
                    else:
                        skipped += 1
                        continue
                if make_parents:
                    _ensure_remote_dir(sftp, posixpath.dirname(target), seen_dirs)
                sftp.put(str(local), target)
                uploaded += 1
            except Exception as exc:  # noqa: BLE001 - report, keep going
                failures.append({"local_path": str(local), "error": str(exc)})

    return {
        "total": len(resolved),
        "uploaded": uploaded,
        "skipped": skipped,
        "failed": len(failures),
        "failures": failures,
    }


@mcp.tool()
def download_file(remote_path: str, local_path: str, overwrite: bool = True) -> str:
    """Download a file from inside the sandbox to local disk.

    Args:
        remote_path: Source path, relative to the sandbox.
        local_path: Destination path on the local filesystem.
        overwrite: If False, fail when the local path already exists.
    """
    source = _resolve(remote_path)
    local = Path(local_path).expanduser()
    if local.exists() and not overwrite:
        raise FileExistsError(f"Local path already exists: {local}")
    local.parent.mkdir(parents=True, exist_ok=True)
    with _Session() as sftp:
        sftp.get(source, str(local))
    return f"Downloaded {source} -> {local} ({local.stat().st_size} bytes)"


@mcp.tool()
def delete_file(remote_path: str) -> str:
    """Delete a single file inside the sandboxed remote directory.

    Refuses to operate on directories (use delete_dir for those).
    """
    target = _resolve(remote_path)
    if target == SANDBOX_ROOT:
        raise PermissionError("Refusing to delete the sandbox root")
    with _Session() as sftp:
        attrs = sftp.stat(target)
        if stat.S_ISDIR(attrs.st_mode or 0):
            raise IsADirectoryError(
                f"{target} is a directory; use delete_dir instead"
            )
        sftp.remove(target)
    return f"Deleted {target}"


@mcp.tool()
def delete_dir(remote_path: str) -> str:
    """Delete an empty directory inside the sandbox.

    The sandbox root itself cannot be deleted.
    """
    target = _resolve(remote_path)
    if target == SANDBOX_ROOT:
        raise PermissionError("Refusing to delete the sandbox root")
    with _Session() as sftp:
        sftp.rmdir(target)
    return f"Removed directory {target}"


@mcp.tool()
def list_files(remote_dir: str = ".") -> list[dict[str, Any]]:
    """List entries in a directory inside the sandbox.

    Args:
        remote_dir: Directory path relative to the sandbox. Defaults to
            the sandbox root.
    """
    target = _resolve(remote_dir)
    with _Session() as sftp:
        entries = sftp.listdir_attr(target)
        return [
            {
                "name": e.filename,
                "size": e.st_size,
                "mtime": e.st_mtime,
                "is_dir": stat.S_ISDIR(e.st_mode or 0),
                "mode": oct(e.st_mode or 0),
            }
            for e in entries
        ]


@mcp.tool()
def make_dir(remote_path: str, mode: int = 0o755, parents: bool = False) -> str:
    """Create a directory inside the sandbox.

    Args:
        remote_path: Directory path relative to the sandbox.
        mode: Octal permission bits (default 0o755).
        parents: If True, create missing intermediate directories too.
    """
    target = _resolve(remote_path)
    if target == SANDBOX_ROOT:
        return f"Sandbox root already exists: {target}"
    with _Session() as sftp:
        if parents:
            parts = target[len(SANDBOX_ROOT) + 1 :].split("/")
            current = SANDBOX_ROOT
            for part in parts:
                current = posixpath.join(current, part)
                try:
                    sftp.stat(current)
                except FileNotFoundError:
                    sftp.mkdir(current, mode)
        else:
            sftp.mkdir(target, mode)
    return f"Created directory {target}"


if __name__ == "__main__":
    mcp.run()
