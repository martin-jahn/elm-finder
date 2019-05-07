from random import randint

import requests
from django.conf import settings
from elm_finder.celery import app


@app.task
def send_to_matomo(ip, user_agent, page_title, page_url, referer, language, country):
    token = settings.MATOMO_TOKEN
    if not token or settings.DEBUG:
        return


    data = {
        "idsite": settings.MATOMO_SITE_ID,
        "token_auth": token,
        "cip": ip,
        "action_name": page_title,
        "url": page_url,
        "rand": randint(0, 1234567890),
        "apiv": 1,
        "urlref": referer,
        "ua": user_agent,
        "lang": language,
        "rec": 1,
    }

    if country:
        data['country'] = country

    r = requests.get(settings.MATOMO_URL, params=data)
