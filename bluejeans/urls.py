from django.urls import path
from .import views

urlpatterns = [
    path('genrate_access_token',views.genrate_access_token , name="genrate_access_token"),
    path('genrate_access_token_for_bluejeans',views.genrate_access_token_for_bluejeans , name="genrate_access_token_for_bluejeans"),
    path('scheduled_meeting',views.scheduled_meeting , name="scheduled_meeting"),
]
