#!/bin/bash
set -eo pipefail
# Makes the Sphinx documentation files

# convert IPython Jupyter notebooks to .rst files
py3 "$SCRIPTS"/ipynb_to_rst.py -s "$SRC"/examples/notebooks -d "$PIFQ"/docs

# generate the documents
uv run sphinx-apidoc -f -o . ../raccoon
# Build HTML docs (equivalent to ./make.bat html)
uv run sphinx-build -M html . _build
set +eo pipefail || exit
