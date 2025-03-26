from django.urls import path, re_path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('create_enquiry', csrf_exempt(views.create_enquiry_api), name="create_enquiry"),
]
