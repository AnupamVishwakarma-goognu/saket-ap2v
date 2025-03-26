from django.urls import path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^$', views.showFollowups, name="showFollowups"),
    re_path(r'^followup_add_details', views.followup_add_details, name="followup_add_details"),
    re_path(r'^followupsCSV', views.followupsCSV, name="followupsCSV"),
    re_path(r'^followup_add_accrodion/(?P<enquiry_id>[\d]+)/(?P<followups_id>[\d]+)/$', views.followup_add_accrodion, name="followup_add_accrodion")
]
