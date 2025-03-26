# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('old-events', views.all_events, name="all_events"),
    path('', views.events, name="events"),
]
