# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib
import inspect
from pathlib import Path

import advent_of_code

project = "advent-of-code-blog"
copyright = "2024, Etienne Schalk"
author = "Etienne Schalk"

html_title = "Advent of Blog"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Automatic documentation generation from code
# https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html
extensions = [
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "autoapi.extension",
    # "sphinx.ext.autosummary",
    "nbsphinx",
    "myst_parser",
    # "sphinxemoji.sphinxemoji",
    # "sphinx_mdinclude",
    "sphinxcontrib.youtube",
    "sphinx_favicon",
    # "sphinxcontrib.github",  # The links to GitHub [source] in API Reference
]

favicons = [{"href": "img/favicon.png"}]

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
    "source_branch": "main",
    "source_directory": "docs/source/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/etienneschalk/advent-of-code/",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
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
    # "private-members", # TODO eschalk improvement -> differentiate more between public and private
    "show-inheritance",
    # "show-module-summary",  # does not look good
    "special-members",
    "imported-members",
]
autoapi_python_class_content = "class"
autoapi_member_order = "bysource"

autodoc_typehints = "signature"  # "description"
autodoc_typehints_format = "short"
# autodoc_typehints_format = "fully-qualified"
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


# based on https://github.com/pydata/xarray/blob/main/doc/conf.py
def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """

    if domain != "py":
        return None

    prefix = "https://github.com/etienneschalk/advent-of-code/tree/main"

    modulename = info["module"]
    fullname = info["fullname"]

    print(f"{info=}")
    print(f"{modulename=}")
    print(f"{fullname=}")

    try:
        submodule = importlib.import_module(modulename)
        # raise Exception
    except Exception:
        print("If submodule cannot be imported, eg because of missing dependency,")
        print("fallback on single URL for whole file")
        # Note: it means that to build the doc with this autolink too,
        # the docs group must be equal to all the dependencies used in the project,
        # making de facto the docs group useless
        url = f"{prefix}/{str(modulename.replace(".", "/"))}.py"

        print(f"{url=}")

        return url

    if submodule is None:
        return None

    print(f"{submodule=}")

    object = submodule
    for part in fullname.split("."):
        try:
            object = getattr(object, part)
        except AttributeError:
            return None

    print(f"{object=}")

    try:
        fn = inspect.getsourcefile(inspect.unwrap(object))  # pyright: ignore[reportArgumentType]
    except TypeError:
        fn = None
    if not fn:
        return None

    print(f"{fn=}")

    try:
        source, lineno = inspect.getsourcelines(object)
    except OSError:
        lineno = None
        source = []

    if lineno:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    try:
        fn_path = Path(fn).relative_to(Path(advent_of_code.__file__).parent.parent)
    except Exception:
        return None

    print(f"{fn_path=}")

    url = f"{prefix}/{str(fn_path)}{linespec}"

    print(f"{url=}")

    return url
