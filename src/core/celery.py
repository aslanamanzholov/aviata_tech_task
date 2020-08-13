from __future__ import (
    absolute_import, unicode_literals
)

from datetime import datetime
from os import environ
from django.utils import timezone
import requests
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.timezone import localtime

environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

headers = {
    'Content-Type': 'application/json'
}

FLIGHT_URL = "https://api.skypicker.com/flights"

IATA_CODES = [{"from": "ALA", "to": "TSE"},
              {"from": "TSE", "to": "ALA"},
              {"from": "ALA", "to": "MOW"},
              {"from": "MOW", "to": "ALA"},
              {"from": "ALA", "to": "CIT"},
              {"from": "CIT", "to": "ALA"},
              {"from": "TSE", "to": "MOW"},
              {"from": "MOW", "to": "TSE"},
              {"from": "TSE", "to": "LED"},
              {"from": "LED", "to": "TSE"}]


class MyCelery(Celery):
    def now(self) -> datetime:
        return localtime()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@periodic_task(run_every=(crontab(minute=0, hour='00')), name="save_flight_to_cache")
def save_flight_to_cache(**kwargs):
    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
    date_to = datetime.today() + timezone.timedelta(days=30)
    date_from = datetime.today().strftime('%d/%m/%Y')
    date_to_converted = date_to.strftime('%d/%m/%Y')
    for i in IATA_CODES:
        cache_name = '{}{}'.format(i['from'], i['to'])
        PARAMS = {
            "fly_from": i['from'],
            "fly_to": i['to'],
            "partner": "picky",
            "partner_market": "us",
            "sort": "price",
            "date_from": date_from,
            "date_to": date_to_converted,
        }
        request = requests.get(FLIGHT_URL, params=PARAMS, headers=headers)
        cache.set(cache_name, request.json(), timeout=CACHE_TTL)
