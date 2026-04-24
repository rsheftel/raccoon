#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- Project information -----------------------------------------------------
project = 'Raccoon'
copyright = '2026, Ryan Sheftel'

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode"
]

# Safely add IPython console highlighting only if IPython is installed
try:
    import IPython  # noqa: F401
    extensions.append("IPython.sphinxext.ipython_console_highlighting")
except ImportError:
    pass  # It's okay if it's not available

# Suppress common duplicate warnings from re-exports
suppress_warnings = [
    "autodoc.duplicate",
    "ref.python",  # for the "more than one target" warnings
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
}

# Make autodoc better with __init__ re-exports
autoclass_content = "both"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# generate docstring for __init__
autoclass_content = 'both'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '**.ipynb_checkpoints']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
