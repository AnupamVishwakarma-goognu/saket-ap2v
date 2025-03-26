from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.recordingclass, name="recordingclass"),
    path('recordingVideo', views.recordingVideo, name="recordingVideo"),
    path('checkout', views.cart_checkout_page, name="cart_checkout_page"),
    path('paymenthandler/', views.paymenthandler, name="paymenthandler"),
    path('recordin_session_record/', views.recordin_session_record, name="recordin_session_record"), 
]