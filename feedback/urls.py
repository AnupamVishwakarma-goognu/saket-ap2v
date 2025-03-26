from django.urls import path, re_path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.feedback, name='feedback'),
]
