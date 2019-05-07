# -*- coding: utf-8 -*-
# Django settings

import os.path
from os import environ

import environ as envmax
from django.template.defaultfilters import slugify

env = envmax.Env()


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

DEBUG = True

# serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = ["127.0.0.1"]

ADMINS = [("Martin Jahn", "martin@jahn.sk")]

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "collected_static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]


# Use the default admin media prefix, which is...
# ADMIN_MEDIA_PREFIX = "/static/admin/"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dj_pagination.middleware.PaginationMiddleware",
]

TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
                "apps.package.context_processors.used_packages_list",
                "apps.grid.context_processors.grid_headers",
                "apps.core.context_processors.current_path",
                "apps.profiles.context_processors.lazy_profile",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "apps.core.context_processors.core_values",
            ]
        },
    }
]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

PROJECT_APPS = [
    "apps.grid",
    "apps.core",
    "apps.homepage",
    "apps.package",
    "apps.profiles",
    "apps.feeds",
    "apps.searchv2",
    "apps.apiv3",
    "utils.matomo",
]

PREREQ_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    # external
    "crispy_forms",
    "dj_pagination",
    "django_extensions",
    "reversion",
    "webstack_django_sorting",
    # "django_modeler",
    "social_django",
    "floppyforms",
    "rest_framework",
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS


MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {"auth.user": lambda o: "/profiles/profile/%s/" % o.username}

AUTH_PROFILE_MODULE = "profiles.Profile"

LOGIN_URL = "/auth/login/github/"
LOGIN_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

CACHE_TIMEOUT = 5 * 60

ROOT_URLCONF = "elm_finder.urls"

SECRET_KEY = "CHANGEME"

URCHIN_ID = ""

DEFAULT_FROM_EMAIL = "Elm finder <elmfinder-noreply@elmfinder.org>"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_SUBJECT_PREFIX = "[Elm finder] "
try:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_PASSWORD = os.environ["SENDGRID_PASSWORD"]
    EMAIL_HOST_USER = os.environ["SENDGRID_USERNAME"]
    EMAIL_PORT = 587
    SERVER_EMAIL = "info@cartwheelweb.com"
    EMAIL_USE_TLS = True
    DEBUG = False
except Exception as e:
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025


PACKAGINATOR_HELP_TEXT = {
    "REPO_URL": "Enter your project repo hosting URL here. Example: https://github.com/martin-jahn/elm-finder",
    "PYPI_URL": "<strong>Leave this blank if this package does not have a PyPI release.</strong> What PyPI uses to index your package. Example: django-uni-form",
}

PACKAGINATOR_SEARCH_PREFIX = "Elm"

# if set to False any auth user can add/modify packages
# only django admins can delete
RESTRICT_PACKAGE_EDITORS = False

# if set to False  any auth user can add/modify grids
# only django admins can delete
RESTRICT_GRID_EDITORS = True


LOCAL_INSTALLED_APPS = []
SUPPORTED_REPO = []

########################## Site specific stuff
FRAMEWORK_TITLE = "Elm"
SITE_TITLE = "Elm finder"

if LOCAL_INSTALLED_APPS:
    INSTALLED_APPS.extend(LOCAL_INSTALLED_APPS)

SUPPORTED_REPO.extend(["bitbucket", "github"])


AUTHENTICATION_BACKENDS = ("social_core.backends.github.GithubOAuth2", "django.contrib.auth.backends.ModelBackend")
GITHUB_API_SECRET = environ.get("GITHUB_API_SECRET")
GITHUB_APP_ID = environ.get("GITHUB_APP_ID")
GITHUB_USERNAME = environ.get("GITHUB_USERNAME")
SOCIAL_AUTH_GITHUB_KEY = GITHUB_APP_ID
SOCIAL_AUTH_GITHUB_SECRET = GITHUB_API_SECRET
SOCIAL_AUTH_ENABLED_BACKENDS = ("github",)
SOCIAL_AUTH_COMPLETE_URL_NAME = "socialauth_complete"
SOCIAL_AUTH_ASSOCIATE_URL_NAME = "associate_complete"
SOCIAL_AUTH_DEFAULT_USERNAME = lambda u: slugify(u)
SOCIAL_AUTH_GITHUB_EXTRA_DATA = []
SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ["username", "first_name", "email"]
LOGIN_REDIRECT_URL = "/"

# associate user via email
# SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

DATABASES = {"default": env.db("DATABASE_URL")}


WSGI_APPLICATION = "elm_finder.wsgi.application"


ADMIN_URL_BASE = environ.get("ADMIN_URL_BASE", r"^admin/")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logutils.colorize.ColorizingStreamHandler',
#             'formatter': 'standard'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': True,
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', ],
#             'propagate': True,
#             'level': 'ERROR',
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         '': {
#             'handlers': ['console', ],
#             'level': os.environ.get('DEBUG_LEVEL', 'ERROR'),
#         },
#     }
# }


URL_REGEX_GITHUB = r"(?:http|https|git)://github.com/[^/]*/([^/]*)/{0,1}"

########### redis setup

# import redis
# from rq import Worker, Queue, Connection

########### end redis setup

########### crispy_forms setup
CRISPY_TEMPLATE_PACK = "bootstrap3"
########### end crispy_forms setup


########### LICENSES from PyPI
LICENSES = """License :: Aladdin Free Public License (AFPL)
License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
License :: DFSG approved
License :: Eiffel Forum License (EFL)
License :: Free For Educational Use
License :: Free For Home Use
License :: Free for non-commercial use
License :: Freely Distributable
License :: Free To Use But Restricted
License :: Freeware
License :: Netscape Public License (NPL)
License :: Nokia Open Source License (NOKOS)
License :: OSI Approved
License :: OSI Approved :: Academic Free License (AFL)
License :: OSI Approved :: Apache Software License
License :: OSI Approved :: Apple Public Source License
License :: OSI Approved :: Artistic License
License :: OSI Approved :: Attribution Assurance License
License :: OSI Approved :: BSD License
License :: OSI Approved :: Common Public License
License :: OSI Approved :: Eiffel Forum License
License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)
License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)
License :: OSI Approved :: GNU Affero General Public License v3
License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)
License :: OSI Approved :: GNU Free Documentation License (FDL)
License :: OSI Approved :: GNU General Public License (GPL)
License :: OSI Approved :: GNU General Public License v2 (GPLv2)
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)
License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
License :: OSI Approved :: IBM Public License
License :: OSI Approved :: Intel Open Source License
License :: OSI Approved :: ISC License (ISCL)
License :: OSI Approved :: Jabber Open Source License
License :: OSI Approved :: MIT License
License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)
License :: OSI Approved :: Motosoto License
License :: OSI Approved :: Mozilla Public License 1.0 (MPL)
License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)
License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
License :: OSI Approved :: Nethack General Public License
License :: OSI Approved :: Nokia Open Source License
License :: OSI Approved :: Open Group Test Suite License
License :: OSI Approved :: Python License (CNRI Python License)
License :: OSI Approved :: Python Software Foundation License
License :: OSI Approved :: Qt Public License (QPL)
License :: OSI Approved :: Ricoh Source Code Public License
License :: OSI Approved :: Sleepycat License
License :: OSI Approved :: Sun Industry Standards Source License (SISSL)
License :: OSI Approved :: Sun Public License
License :: OSI Approved :: University of Illinois/NCSA Open Source License
License :: OSI Approved :: Vovida Software License 1.0
License :: OSI Approved :: W3C License
License :: OSI Approved :: X.Net License
License :: OSI Approved :: zlib/libpng License
License :: OSI Approved :: Zope Public License
License :: Other/Proprietary License
License :: Public Domain
License :: Repoze Public License""".splitlines()
########### End LICENSES from PyPI


########## GITHUB
GITHUB_API_SECRET = environ.get("GITHUB_API_SECRET")
GITHUB_APP_ID = environ.get("GITHUB_APP_ID")
GITHUB_TOKEN = environ.get("GITHUB_TOKEN")

########### SECURITY
ALLOWED_HOSTS = ["*"]

REST_FRAMEWORK = {"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination", "PAGE_SIZE": 20}


CELERY_BROKER_URL = "redis://localhost:6379/4"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_IGNORE_RESULT = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ["json"]


MATOMO_TOKEN = environ.get("MATOMO_TOKEN")
MATOMO_URL = environ.get("MATOMO_URL")
MATOMO_SITE_ID = environ.get("MATOMO_SITE_ID")
