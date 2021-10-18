#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

DEFAULT_LANG = 'en'

AUTHOR = 'Daniel Rothenberg'
SITENAME = "daniel rothenberg"
SITEURL = 'https://www.danielrothenberg.com'

# Time and dates
TIMEZONE = 'US/Eastern'
DATE_FORMATS = {
    'en': "%B %d, %Y"
}

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = "http://github.com/darothen"
TWITTER_USERNAME = "danrothenberg"
DEFAULT_PAGINATION = 4

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_ALL_RSS = None # "feeds/all.rss.xml"
CATEGORY_FEED_RSS = None # "feeds/%s.rss.xml"

# Blogroll
LINKS =  ()

# Social widget
SOCIAL = (
    ('twitter', 'http://twitter.com/danrothenberg'),
    ('github', 'http://github.com/darothen'),
    ('linkedin', 'https://www.linkedin.com/in/rothenbergdaniel'),
    ('researchgate', 'https://www.researchgate.net/profile/Daniel_Rothenberg'),
    ('mendeley', 'https://www.mendeley.com/profiles/daniel-rothenberg1/'),
    ('orcid', 'http://orcid.org/0000-0002-8270-4831'),
)

# Theming
THEME = "pelican-darothen"
BOOTSTRAP_THEME = "yeti"
HIDE_SIDEBAR = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
BANNER = "/images/2015/06/cropped-copy-header_final-bordered.jpg"

# Static content
STATIC_PATHS = ['images', ]

# Page / Blog configuration
DISPLAY_PAGES_ON_MENU = True
DEFAULT_CATEGORY = 'blog'
USE_FOLDER_AS_CATEGORY = True

DIRECT_TEMPLATES = [
    'index', 'archives',
]
PAGINATED_TEMPLATES = [
    'blog',
]
ARCHIVES_SAVE_AS = 'archives.html'


ARTICLE_URL = "blog/{date:%Y}/{date:%b}/{slug}/"
ARTICLE_SAVE_AS =  "blog/{date:%Y}/{date:%b}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"


# Plugins
from pelican_jupyter import liquid as nb_liquid
PLUGIN_PATHS = ['./pelican-plugins', ]
PLUGINS = [
    'liquid_tags.img', 
    'liquid_tags.video',
    'liquid_tags.youtube',
    'liquid_tags.vimeo',
    'liquid_tags.include_code', 
    nb_liquid, 
]
IGNORE_FILES = [".ipynb_checkpoints"]
# NOTE: This was deprecated in the switch to pelican-jupyter and we now need to
#       manually prepend notebook paths with "notebooks/"
# NOTEBOOK_DIR = 'notebooks'
try:
    EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8') if os.path.exists('_nb_header.html') else None
except:
    pass
