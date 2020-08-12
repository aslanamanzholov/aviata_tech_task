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
BOOKING_URL = "https://booking-api.skypicker.com/api/v0.1/check_flights"

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
        adults = self.request.data['adults']
        infants = self.request.data['infants']

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
            if 'data' in data and data['data'] is not None and data['data']:
                # if sort from request is not valid
                minimum = min(i['price'] for i in data['data'])
                maximum = max(i['price'] for i in data['data'])
                cheaper = maximum - minimum

                print({"MIN": minimum, "MAX": maximum, "AVG": cheaper})

                for i in data['data']:
                    if 'price' in i and i['price'] is not None:
                        if len(arr) >= 10:
                            break
                        request_for_booking = requests.get(BOOKING_URL, params={"booking_token": i['booking_token']},
                                                           headers=headers).json()
                        if 'flights_invalid' in request_for_booking and \
                                request_for_booking['flights_invalid'] is not True \
                                and request_for_booking['price_change'] is not True:
                            arr.append(i)
                cache.set(fly_from + fly_to + date_f + date_t, request.json(), timeout=CACHE_TTL)
                return Response({"details": arr}, status=status.HTTP_201_CREATED)
            else:
                return Response({"details": data})
