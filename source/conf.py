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
import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'TIL'
copyright = '2019 - 2021, MusicScience37 (Kenta Kabashima). Licensed under the CC BY 4.0'
author = 'MusicScience37'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# setting of todo
extensions += ['sphinx.ext.todo']
todo_include_todos = True

# setting of mathjax
extensions += ['sphinx.ext.mathjax']
# force to use MathJax 2 for compatibility with Plotly
mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
mathjax_config = {
    'TeX': {
        'Macros': {
            'bm': ['{\\boldsymbol{#1}}', 1],
        },
    },
}

# setting of PlantUML
extensions += ['sphinxcontrib.plantuml']
plantuml_jar_path = os.getenv("PLANTUML_JAR_PATH")
plantuml = 'java -jar ' + plantuml_jar_path
plantuml_output_format = 'svg'
plantuml_syntax_error_image = True

# setting of jupyter-sphinx
extensions += ['jupyter_sphinx']
if sys.platform == 'win32':
    # required on Windows
    # https://stackoverflow.com/questions/58422817/jupyter-notebook-with-python-3-8-notimplementederror
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# setting of opengraph
# https://pypi.org/project/sphinxext-opengraph/
extensions += ['sphinxext.opengraph']
ogp_site_url = 'https://til.musicscience37.com/'
ogp_site_name = "MusicScience37's TIL"
ogp_image = 'https://til.musicscience37.com/_static/KIcon80white.png'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ja'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'KIcon/*'
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_title = 'MusicScience37\'s TIL'

html_logo = 'KIcon/KIcon80white.png'
html_favicon = 'KIcon/KIcon.ico'

html_theme_options = {
    'style_nav_header_background': '#B24700',
}

html_css_files = ['til-custom.css']
