# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Katonic'
copyright = '2020, Katonic'
author = 'Katonic'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

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

import sphinx_theme_pd
html_theme = 'sphinx_theme_pd'
html_theme_path = [sphinx_theme_pd.get_html_theme_path()]

# -- Options for EPUB output
epub_show_urls = 'footnote'
