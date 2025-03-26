# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_testimonials, name="testimonials"),
]
