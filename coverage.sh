#!/bin/bash

# This only works in Cygwin on Windows
# Excludes slow tests

py3 -m pytest --color=yes --cov=raccoon --cov-report html
cygstart htmlcov/index.html
