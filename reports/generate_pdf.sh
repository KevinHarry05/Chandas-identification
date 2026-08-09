#!/usr/bin/env bash
# generate_pdf.sh - generate a PDF from the Markdown report using pandoc + xelatex

set -euo pipefail
INPUT="reports/Chandas_Report.md"
OUTPUT="reports/Chandas_Report.pdf"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is not installed. Install pandoc and a TeX engine (e.g., texlive or tinytex)."
  exit 1
fi

pandoc "$INPUT" -o "$OUTPUT" --pdf-engine=xelatex --metadata title="A Language-Aware Neural Framework for Cross-Lingual Prosodic Analysis of Sanskrit and Tamil Poetry"

echo "PDF generated at $OUTPUT"
