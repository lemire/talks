# ssh-mcp

A small [Model Context Protocol](https://modelcontextprotocol.io) server that
lets an AI assistant manage files on a remote server over SSH/SFTP. All
operations are **sandboxed**: the assistant can only read, write, list, or
delete things inside the single `remotedirectory` named in `credentials.json`.
Any attempt to step outside (via `..`, absolute paths, etc.) is rejected.

## Tools exposed

| Tool            | Purpose                                                 |
| --------------- | ------------------------------------------------------- |
| `sandbox_info`  | Show the sandbox root and connection target.            |
| `list_files`    | List entries in a directory inside the sandbox.         |
| `upload_file`   | Upload a local file into the sandbox.                   |
| `download_file` | Download a file from the sandbox to local disk.         |
| `delete_file`   | Delete a single file inside the sandbox.                |
| `delete_dir`    | Remove an empty directory inside the sandbox.           |
| `make_dir`      | Create a directory inside the sandbox (`parents=True` supported). |

Paths passed to any tool are interpreted **relative to the sandbox root**.
An absolute path is accepted only if it already lies inside the sandbox.

## Requirements

- Python **3.10+**
- [`uv`](https://docs.astral.sh/uv/) — the script declares its dependencies
  inline ([PEP 723](https://peps.python.org/pep-0723/)), and `uv run` resolves
  them automatically on first launch. Install with:

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  (If you'd rather use plain `pip`, install `mcp[cli]>=1.2.0` and
  `paramiko>=3.4.0` into a venv and replace the launch command below with
  `python /absolute/path/to/server.py`.)

## Configuration — `credentials.json`

Create `credentials.json` **next to `server.py`** (this directory). Minimum:

```json
{
  "host": "example.com",
  "username": "myuser",
  "remotedirectory": "/home/myuser/uploads"
}
```

Full set of supported fields:

| Field                       | Required | Default | Description                                                                  |
| --------------------------- | -------- | ------- | ---------------------------------------------------------------------------- |
| `host`                      | yes      | —       | SSH hostname.                                                                |
| `username`                  | yes      | —       | SSH user.                                                                    |
| `remotedirectory`           | yes      | —       | Absolute path on the server — the **sandbox root**.                          |
| `port`                      | no       | `22`    | SSH port.                                                                    |
| `key_path`                  | no       | —       | Path to a private key (e.g. `~/.ssh/id_ed25519`).                            |
| `passphrase`                | no       | —       | Passphrase for the private key, if encrypted.                                |
| `password`                  | no       | —       | Password authentication (prefer keys when possible).                         |
| `known_hosts`               | no       | system  | Path to an additional `known_hosts` file.                                    |
| `strict_host_key_checking`  | no       | `true`  | When `false`, unknown host keys are auto-accepted (use only for first run).  |

When `key_path` and `password` are both omitted, the SSH agent and the
default keys in `~/.ssh/` are tried.

Keep this file out of git — add to `.gitignore`:

```
credentials.json
```

## Wiring it into Claude Code

Claude Code reads MCP server definitions from `~/.claude.json` (or
`~/.config/claude-code/config.json` depending on version) or from a
project-local `.mcp.json`. Add an entry like:

```json
{
  "mcpServers": {
    "ssh-files": {
      "command": "/Users/dlemire/CVS/github/talks/2026/quebec/ssh-mcp/server.py"
    }
  }
}
```

The PEP 723 shebang (`#!/usr/bin/env -S uv run --script`) makes the file
directly executable — `uv` materialises the dependencies in a cached
virtual environment on first call. Alternatively, be explicit:

```json
{
  "mcpServers": {
    "ssh-files": {
      "command": "uv",
      "args": [
        "run",
        "--script",
        "/Users/dlemire/CVS/github/talks/2026/quebec/ssh-mcp/server.py"
      ]
    }
  }
}
```

You can also register it from the CLI:

```sh
claude mcp add ssh-files /Users/dlemire/CVS/github/talks/2026/quebec/ssh-mcp/server.py
```

Restart Claude Code, then check:

```sh
claude mcp list
```

You should see `ssh-files` connected, and the tools listed above will be
available to the model.

## Wiring it into Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows) and
add the same `mcpServers` block as above, then fully quit and relaunch
Claude Desktop.

## Wiring it into other MCP-compatible clients

Most clients (Cursor, Cline, Zed, Continue, etc.) accept the same JSON
shape — a server entry with `command` and optional `args`/`env`. Point
the `command` at this `server.py`. Because the script speaks MCP over
stdio, no port or URL needs to be configured.

## Quick smoke test

From this directory, with a valid `credentials.json` in place:

```sh
# Verify dependencies resolve and the script starts.
uv run --script server.py --help 2>/dev/null || echo "ready"

# Inspect tools interactively with the MCP inspector:
npx @modelcontextprotocol/inspector uv run --script ./server.py
```

The inspector gives you a web UI where you can call each tool by hand —
useful for verifying that `sandbox_info` reports the right root and that
`list_files` works before handing the server to an AI.

## Security notes

- The sandbox is enforced by normalising every supplied path and rejecting
  anything that does not stay under `remotedirectory`. This stops `..`
  traversal in tool arguments.
- It does **not** override what the SSH user account itself is allowed to
  do on the server. If the account has broader filesystem access and the
  remote directory contains symlinks pointing outside it, those symlinks
  could still be followed by the SFTP server. For maximum confinement,
  ensure the sandbox directory contains no outbound symlinks (or use an
  SSH account that is `chroot`-jailed at the SSH daemon level).
- Prefer key-based auth and keep `credentials.json` out of version control.
