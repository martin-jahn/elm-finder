import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DOMAIN = "www.elmfinder.org"
ALLOWED_HOSTS = [DOMAIN]
CSRF_COOKIE_DOMAIN = DOMAIN
SESSION_COOKIE_DOMAINS = DOMAIN

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE


DEBUG = False

# serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.CachedStaticFilesStorage"

RESTRICT_PACKAGE_EDITORS = False
RESTRICT_GRID_EDITORS = True


### Sentry settings

sentry_sdk.init(dsn=environ.get("SENTRY_DSN"), integrations=[DjangoIntegration()])

### End Sentry


SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


########## CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        },
    }
}


# If not defined create random key in production default in base.py is pretty terrible idea
if not hasattr(globals(), "SECRET_KEY"):
    SECRET_FILE = os.path.join(PROJECT_ROOT, "secret.txt")
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            import string

            symbols = "".join((string.ascii_lowercase, string.digits, string.punctuation))
            SECRET_KEY = "".join([choice(symbols) for i in range(50)])
            with open(SECRET_FILE, "w") as secret:
                secret.write(SECRET_KEY)
                secret.close()
        except IOError:
            raise Exception("Please create a %s file with random characters to generate your secret key!" % SECRET_FILE)
