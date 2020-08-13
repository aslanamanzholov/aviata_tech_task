from django.conf import settings
from rest_framework import serializers


class FlightSerializer(serializers.Serializer):
    fly_from = serializers.CharField()
    fly_to = serializers.CharField()
    adults = serializers.IntegerField(default=0)
    children = serializers.IntegerField(default=0)
    infants = serializers.IntegerField(default=0)
    date_from = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_to = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS)
