import csv
import datetime
import json

import requests

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import FlightSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

FLIGHT_URL = "https://api.skypicker.com/flights"

headers = {
    'Content-Type': 'application/json'
}


class FlightViewSet(GenericAPIView):
    serializer_class = FlightSerializer

    def post(self, request):
        fly_to = self.request.data['fly_to']
        fly_from = self.request.data['fly_from']
        date_f = self.request.data['date_from']
        date_t = self.request.data['date_to']
        adults = (self.request.data['adults'], 1)
        infants = (self.request.data['infants'], 1)

        date_from = datetime.datetime.strptime(date_f, '%Y-%m-%d').strftime('%d/%m/%Y')
        date_to = datetime.datetime.strptime(date_t, '%Y-%m-%d').strftime('%d/%m/%Y')

        PARAMS = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "partner": "picky",
            "partner_market": "us",
            "date_from": date_from,
            "date_to": date_to,
            "sort": "price",
            "adults": adults,
            "infants": infants
        }

        if fly_from + fly_to + date_f + date_t in cache:
            # get results from cache
            flights = cache.get(fly_from + fly_to + date_f + date_t)
            return Response(flights, status=status.HTTP_201_CREATED)
        else:
            request = requests.get(FLIGHT_URL, params=PARAMS, headers=headers)
            data = request.json()
            arr = []
            if data['data']:
                minim = min(i['price'] for i in data['data'])
                maxim = max(i['price'] for i in data['data'])
                print(minim)
                cheaper = maxim - minim
                for i in data['data']:
                    if i['price'] and i['price'] is not None:
                        if i['price'] <= cheaper:
                            arr.append(i)
                            if len(arr) >= 10:
                                break
            cache.set(fly_from + fly_to + date_f + date_t, request.json(), timeout=CACHE_TTL)
            return Response({"details": arr}, status=status.HTTP_201_CREATED)
