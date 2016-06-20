#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

DEFAULT_LANG = 'en'

AUTHOR = 'Daniel Rothenberg'
SITENAME = "Daniel Rothenberg's Homepage"
SITEURL = 'http://www.danielrothenberg.com'
TIMEZONE = 'US/Eastern'

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

# Themes
THEME = "pelican-bootstrap3"
BOOTSTRAP_THEME = "yeti"

# Static content
STATIC_PATHS = ['images', ]

ARTICLE_URL = "blog/{date:%Y}/{date:%b}/{slug}/"
ARTICLE_SAVE_AS =  "blog/{date:%Y}/{date:%b}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
