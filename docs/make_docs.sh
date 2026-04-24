#!/bin/bash
set -eo pipefail
# Makes the Sphinx documentation files

# convert IPython Jupyter notebooks to .rst files
export PATH="$PATH:/c/Program Files/Pandoc"
uv run --no-sync jupyter nbconvert --to rst --execute --output-dir . --output usage_dataframe.rst ../examples/usage_dataframe.ipynb
uv run --no-sync jupyter nbconvert --to rst --execute --output-dir . --output usage_series.rst ../examples/usage_series.ipynb
uv run --no-sync jupyter nbconvert --to rst --execute --output-dir . --output speed_test.rst ../examples/speed_test.ipynb
uv run --no-sync jupyter nbconvert --to rst --execute --output-dir . --output convert_pandas.rst ../examples/convert_pandas.ipynb

# generate the documents
uv run sphinx-apidoc -f -o . --separate --module-first ../raccoon
# Build HTML docs (equivalent to ./make.bat html)
uv run sphinx-build -M html . _build
set +eo pipefail || exit
