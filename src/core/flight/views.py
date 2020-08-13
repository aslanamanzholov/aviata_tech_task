import logging
from datetime import datetime as hi
import requests

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import FlightSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

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
        adults = int(self.request.data['adults'])
        infants = int(self.request.data['infants'])
        children = int(self.request.data['children'])
        pnum = adults + children + infants

        cache_name = '{}{}'.format(fly_from, fly_to)

        if cache_name in cache:
            try:
                # get results from cache
                flights = cache.get(cache_name)
                arr = []
                if 'data' in flights and flights['data'] is not None and flights['data']:
                    # if sort from request is not valid
                    minimum = min(i['price'] for i in flights['data'])
                    maximum = max(i['price'] for i in flights['data'])
                    cheaper = maximum - minimum

                    print({"MIN": minimum, "MAX": maximum, "AVG": cheaper})

                    for i in flights['data']:
                        if 'price' in i and i['price'] is not None:
                            test = hi.fromtimestamp(i['dTimeUTC']).isoformat()
                            if date_f <= test <= date_t:
                                if len(arr) >= 10:
                                    break
                                request_for_booking = requests.get(BOOKING_URL, params={"booking_token": i['booking_token'],
                                                                                        "adults": adults, "children": children,
                                                                                        "infants": infants, "pnum": pnum,
                                                                                        "bnum": 0},
                                                                   headers=headers).json()
                                if 'flights_invalid' in request_for_booking and \
                                        request_for_booking['flights_invalid'] is not True \
                                        and request_for_booking['price_change'] is not True:
                                    arr.append(i)
                    return Response({"details": arr}, status=status.HTTP_200_OK)
            except Exception as e:
                logging.critical(e, exc_info=True)
        else:
            return Response({"details": "Не найдено"})
