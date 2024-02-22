import os

AUTHOR = "Daniel Rothenberg"
SITENAME = "daniel rothenberg"
SITEURL = ""
# SITEURL = "https://www.danielrothenberg.com"

PATH = "content"

TIMEZONE = "America/Denver"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
    ("twitter", "http://twitter.com/danrothenberg"),
    ("github", "http://github.com/darothen"),
    ("linkedin", "https://www.linkedin.com/in/rothenbergdaniel"),
    ("researchgate", "https://www.researchgate.net/profile/Daniel_Rothenberg"),
    ("mendeley", "https://www.mendeley.com/profiles/daniel-rothenberg1/"),
    ("orcid", "http://orcid.org/0000-0002-8270-4831"),
)

# Theming
THEME = "pelican-darothen"
BOOTSTRAP_THEME = "yeti"
HIDE_SIDEBAR = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
BANNER = "images/banner.jpg"

# Static content
STATIC_PATHS = [
    "images",
]

# Page / Blog configuration
DISPLAY_PAGES_ON_MENU = True
DEFAULT_CATEGORY = "blog"
USE_FOLDER_AS_CATEGORY = True

DIRECT_TEMPLATES = []
PAGINATED_TEMPLATES = []
ARCHIVES_SAVE_AS = None


ARTICLE_URL = "blog/{date:%Y}/{date:%b}/{slug}/"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%b}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

DEFAULT_PAGINATION = 4

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Plugins
PLUGIN_PATHS = [
    "./pelican-plugins",
]
PLUGINS = []
IGNORE_FILES = [".ipynb_checkpoints"]
# NOTE: This was deprecated in the switch to pelican-jupyter and we now need to
#       manually prepend notebook paths with "notebooks/"
# NOTEBOOK_DIR = 'notebooks'
EXTRA_HEADER = (
    open("_nb_header.html").read() if os.path.exists("_nb_header.html") else None
)
