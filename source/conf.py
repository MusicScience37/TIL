# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os

# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "TIL"
copyright = (
    "2019 - 2024, MusicScience37 (Kenta Kabashima). Licensed under the CC BY 4.0"
)
author = "MusicScience37"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# setting of todo
extensions += ["sphinx.ext.todo"]
todo_include_todos = True

# settings of myst-nb
extensions += ["myst_nb"]  # This will automatically include myst_parser
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]
nb_execution_mode = "cache"
nb_execution_cache_path = "build/jupyter_cache"
nb_output_stderr = "remove-warn"

# setting of MathJax
# Extension for MathJax is already enabled by myst_nb.
# MathJax URL working with Plotly was written in https://www.npmjs.com/package/plotly.js/v/2.16.4#mathjax.
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
mathjax3_config = {
    "tex": {
        "macros": {
            "bm": ["{\\boldsymbol{#1}}", 1],
        },
    },
}

# setting of PlantUML
extensions += ["sphinxcontrib.plantuml"]
plantuml_jar_path = os.getenv("PLANTUML_JAR_PATH")
plantuml = "java -jar " + plantuml_jar_path
plantuml_output_format = "svg"
plantuml_syntax_error_image = True

# setting of opengraph
# https://pypi.org/project/sphinxext-opengraph/
extensions += ["sphinxext.opengraph"]
ogp_site_url = "https://til.musicscience37.com/"
ogp_site_name = "MusicScience37's TIL"
ogp_image = "https://kicon.musicscience37.com/KIcon128white.png"

# setting of bibtex
# https://sphinxcontrib-bibtex.readthedocs.io/
extensions += ["sphinxcontrib.bibtex"]
bibtex_bibfiles = ["bibliography.bib"]
bibtex_default_style = "plain"
bibtex_reference_style = "super"

# settings of trimblank
# https://pypi.org/project/sphinxcontrib-trimblank/
extensions += ["sphinxcontrib.trimblank"]
trimblank_keep_alnum_blank = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_orange_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    "_static",
]

# Required for plotly.
html_js_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"
]

html_title = "MusicScience37's TIL"

html_logo = "https://kicon.musicscience37.com/KIcon80.png"
html_favicon = "https://kicon.musicscience37.com/KIcon.ico"

html_theme_options = {
    "show_prev_next": False,
    "logo": {
        "text": html_title,
    },
    "pygment_light_style": "gruvbox-light",
    "pygment_dark_style": "native",
    "repository_url": "https://gitlab.com/MusicScience37/til",
    "use_repository_button": True,
    "use_source_button": True,
    "path_to_docs": "source",
}
