# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'chipyard-dataflow'
copyright = '2025, Dahu Feng'
author = 'Dahu Feng'
release = 'v0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

language = 'zh_CN'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'pydata_sphinx_theme'
html_title = project

html_theme = "sphinx_book_theme"
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# html_theme = 'sphinx_rtd_theme'
html_logo = "assets/logo/chipyard-dataflow.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_theme_options = {
    "path_to_docs": "../source",
    "repository_url": "https://github.com/FDH21/chipyard-dataflow",
    "repository_provider": "github",
    "use_repository_button": True,
}
extensions = ["sphinx_markdown_tables", "sphinx.ext.napoleon", "sphinx.ext.viewcode", "sphinx.ext.intersphinx", "sphinx_copybutton",
"sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinxarg.ext", "sphinxcontrib.redoc", "myst_parser"]
    # "sphinx.ext.napoleon",
    # "sphinx.ext.viewcode",
    # "sphinx.ext.intersphinx",
    # "sphinx_copybutton",
    # "sphinx.ext.autodoc",
    # "sphinx.ext.autosummary",
    # "myst_parser",
    # "sphinxarg.ext",
    # "sphinxcontrib.redoc"]
