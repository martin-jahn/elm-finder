from apps.searchv2.builders import build_index as build
from elm_finder.celery import app


@app.task
def build_index():
    build()
