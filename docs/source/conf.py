# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "advent-of-code-blog"
copyright = "2024, Etienne Schalk"
author = "Etienne Schalk"

html_title = "Advent of Blog"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Automatic documentation generation from code
# https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html
extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "autoapi.extension",
    "nbsphinx",
    "myst_parser",
    # "sphinxemoji.sphinxemoji",
    # "sphinx_mdinclude",
    "sphinxcontrib.youtube",
]

source_suffix = [".rst", ".md"]

nbsphinx_allow_errors = True

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

html_theme_options = {
    "announcement": "🚧 This blog is work in progress",
    "light_logo": "img/light-logo_arr_3x_red_filled_from_center.png",
    "dark_logo": "img/dark-logo_arr_3x_red_filled_from_center.png",
    "source_repository": "https://github.com/etienneschalk/advent-of-code/",
}

pygments_style = "default"
pygments_dark_style = "monokai"

# API Reference Generation

# https://sphinx-autoapi.readthedocs.io/en/latest/
# https://bylr.info/articles/2022/05/10/api-doc-with-sphinx-autoapi/
autoapi_generate_api_docs = True
autoapi_dirs = ["../../advent_of_code"]
autoapi_type = "python"
# autoapi_keep_files = True
# autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "show-inheritance",
    # "show-module-summary",
    "special-members",
    "imported-members",
]
autodoc_typehints = "signature"  # "description"
autodoc_typehints_format = "short"
autodoc_inherit_docstrings = False
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True
# Do not show fully qualified paths to classes and functions
add_module_names = False

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    # Numpy seems broken
    "python": ("https://docs.python.org/3.12/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "xarray": ("https://xarray.pydata.org/en/stable/", None),
}

myst_enable_extensions = ["deflist", "tasklist"]
