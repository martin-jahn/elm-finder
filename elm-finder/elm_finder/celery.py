import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elm_finder.settings.development")
app = Celery("elm_finder")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
