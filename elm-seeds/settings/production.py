from .base import *

ALLOWED_HOSTS = ["www.elmseeds.org"]


DEBUG = False

# serve media through the staticfiles app.
SERVE_MEDIA = DEBUG


RESTRICT_PACKAGE_EDITORS = False
RESTRICT_GRID_EDITORS = True


### Sentry settings

INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
RAVEN_MIDDLEWARE = ["raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware"]
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE
SENTRY_DSN = env("DJANGO_SENTRY_DSN")
SENTRY_CLIENT = env("DJANGO_SENTRY_CLIENT", default="raven.contrib.django.raven_compat.DjangoClient")

### End Sentry


TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        ("django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"),
    )
]
