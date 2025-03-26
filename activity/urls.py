from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.activity, name="activity"),
    path('result', views.result, name="result"),
]
