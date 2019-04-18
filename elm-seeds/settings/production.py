import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ALLOWED_HOSTS = ["www.elmseeds.org"]


DEBUG = False

TEMPLATES[0]["OPTIONS"]["DEBUG"] = DEBUG

# serve media through the staticfiles app.
SERVE_MEDIA = DEBUG


RESTRICT_PACKAGE_EDITORS = False
RESTRICT_GRID_EDITORS = True


### Sentry settings

sentry_sdk.init(dsn=environ.get("SENTRY_DSN"), integrations=[DjangoIntegration()])

### End Sentry


TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        ("django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"),
    )
]


SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
