from .base import *

RESTRICT_PACKAGE_EDITORS = False
RESTRICT_GRID_EDITORS = False


### Debug toolbar settings

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS += ("debug_toolbar",)

INTERNAL_IPS = ("127.0.0.1",)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False, "SHOW_TEMPLATE_CONTEXT": True}

### End Debug toolbar
