from django.conf.urls import url
from django.urls import path

from .views import FlightViewSet

urlpatterns = [
    path(route='', view=FlightViewSet.as_view()),
]
