# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.learning_path_listing,name="learning-path-listing"),
    path('<slug:slug>',views.learning_path_details,name="learning-path-detail"),
    ]
