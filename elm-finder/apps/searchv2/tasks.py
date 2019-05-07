from elm_finder.celery import app

from apps.searchv2.builders import build_index as build


@app.task
def build_index():
    build()
