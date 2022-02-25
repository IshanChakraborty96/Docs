# Configuration file for the Sphinx documentation builder.
from datetime import datetime

# -- Project information

project = 'Katonic'
copyright = '2020, Katonic'
author = 'Katonic'

release = '1.0.0'
version = '1.0.1'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output

# import sphinx_theme_pd
#xclude_patterns = ["_build"]
#html_theme = "insegel"
#html_theme_options = {"navigation_depth": 2}

html_logo = "Logo.svg"

# -- Options for EPUB output
epub_show_urls = 'footnote'

