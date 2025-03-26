from django.urls import path
from .import views


urlpatterns = [
    path("",views.report,name="report"),
    path("get_report",views.get_report,name="get_report"),
    path("fee_collection",views.fee_collection,name="fee_collection"),
]