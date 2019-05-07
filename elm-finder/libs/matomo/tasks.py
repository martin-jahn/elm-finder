from random import randint

import requests
from django.conf import settings
from elm_finder.celery import app


@app.task
def send_to_matomo(tracking_data, response_time):
    token = settings.MATOMO_TOKEN
    if not token:
        return

    data = {
        "idsite": settings.MATOMO_SITE_ID,
        "token_auth": token,
        "cip": tracking_data["ip"],
        "action_name": tracking_data["page_title"],
        "url": tracking_data["url"],
        "rand": randint(0, 1234567890),
        "apiv": 1,
        "urlref": tracking_data["referer"],
        "ua": tracking_data["user_agent"],
        "lang": tracking_data["language"],
        "rec": 1,
        "gt_ms": response_time,
    }

    try:
        data.update(tracking_data["extra"])
    except KeyError:
        pass

    if not tracking_data["country"]:
        tracking_data.pop("country")

    requests.get(settings.MATOMO_URL, params=data)
