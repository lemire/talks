#!/bin/bash
# marpit.sh: Build Marp talks to HTML and generate index
set -e
# Change to the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Create public directory if not present
mkdir -p public
grep -v '^#' .marp-talks | while IFS= read -r file; do
  echo "seen $file"
done


# Build Marp talks to HTML
files=()
while IFS= read -r line; do
  files+=("$line")
done < <(grep -v '^#' .marp-talks)  # Extract lines to an array

for file in "${files[@]}"; do
  file="$(echo "$file" | xargs)"  # Trim whitespace at the beginning and end of the line
  echo "Processing $file"
  [ -z "$file" ] && continue
  # Vérification que le fichier existe
  if [ ! -f "$file" ]; then
    echo "File $file does not exist. Skipping."
    continue
  fi
  # Relative path without extension
  relpath="${file%.md}"
  # Source directory (where the .md is)
  srcdir=$(dirname "$file")
  # Target directory in public/
  dstdir="public/$srcdir"
  mkdir -p "$dstdir"
  # Copy all contents from the source directory (files and subdirectories)
  if [ -d "$srcdir" ]; then
    cp -r "$srcdir"/* "$dstdir"/ 2>/dev/null || true
  fi
  # Generate the HTML and PDF in the target directory
  out_html="$(basename "$file" .md).html"
  out_pdf="$(basename "$file" .md).pdf"
  marp --html --allow-local-files "$file" -o "$dstdir/$out_html"
  marp --pdf --allow-local-files "$file" -o "$dstdir/$out_pdf"

  # Check if HTML file was generated and report its size
  htmlpath="$dstdir/$out_html"
  if [ -f "$htmlpath" ]; then
    size=$(stat -c %s "$htmlpath" 2>/dev/null || stat -f %z "$htmlpath" 2>/dev/null)
    echo "Generated $htmlpath ($size bytes)"
  else
    echo "File $htmlpath was not generated."
  fi

  # Check if PDF file was generated and report its size
  pdfpath="$dstdir/$out_pdf"
  if [ -f "$pdfpath" ]; then
    size=$(stat -c %s "$pdfpath" 2>/dev/null || stat -f %z "$pdfpath" 2>/dev/null)
    echo "Generated $pdfpath ($size bytes)"
  else
    echo "File $pdfpath was not generated."
  fi
done

echo "All talks processed."
# Add index.html listing all talks
echo '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Daniel Lemire&#39;s talks</title><link rel="stylesheet" href="styles.css"></head><body><h1>Daniel Lemire&#39;s talks</h1>' > public/index.html
# Collect all talks and years
awk 'BEGIN{FS="/"} /^[^#]/ && NF>0 { year=$1; talks[year]=talks[year] $0 "\n"; years[year]=1 } END { for (y in years) print y }' .marp-talks | sort -r > years.txt
while read year; do
  [ -z "$year" ] && continue
  echo "<h2>$year</h2><ul>" >> public/index.html
  grep "^$year/" .marp-talks | while read file; do
    [ -z "$file" ] && continue
    case "$file" in \#*) continue ;; esac
    relpath="${file%.md}"
    htmlpath="$relpath.html"
    pdfpath="$relpath.pdf"
    title=$(grep -m 1 '^title:' "$file" | sed 's/^title: //')
    description=$(grep -m 1 '^description:' "$file" | sed 's/^description: //')
    echo "<li><a href='$htmlpath' title='$description'>$title</a> <a href='$pdfpath' title='$description'>PDF</a></li>" >> public/index.html
  done
  echo "</ul>" >> public/index.html
done < years.txt
rm years.txt
echo '</body></html>' >> public/index.html
cp css/styles.css public/ || true
