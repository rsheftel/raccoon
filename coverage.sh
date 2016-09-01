#!/bin/bash

# This only works in Cygwin on Windows
# Excludes slow tests

py3 -m pytest --color=yes --cov=raccoon --cov-report html
cygstart $TEMP/raccoon_coverage_report/index.html
