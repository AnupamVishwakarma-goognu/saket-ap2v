from django.urls import path, re_path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    
    re_path(r'^list/', views.EnquiryListView.as_view(), name="list_enquiry"),
    re_path(r'^enquiries_filter', views.enquiries_filter, name="enquiries_filter"),
    re_path(r'^table_data_filter', views.table_data_filter, name="table_data_filter"),
    re_path(r'^discard/followups/(?P<pk>\d+)/$', csrf_exempt(views.DiscardFollowupsView.as_view()), name="DiscardFollowupsView"),
    re_path(r'^view/(?P<enquiries_id>[\w]+)/$', views.view, name="enquiry_view"),
    re_path(r'^followups/(?P<followup_id>[\w]+)/$', views.addFollowUps, name="followUps"),
    re_path(r'^add_course/(?P<enquiries_id>[\d]+)/$', views.add_course, name="add_course"),
    re_path(r'^discard/enquiry/(?P<pk>\d+)/$', csrf_exempt(views.DiscardEnquiryView.as_view()), name="DiscardEnquiryView"),
    re_path(r'^enquiry_update/(?P<enquiry_update_id>[\d]+)/$', views.update_enquiry, name="update_enquiry"),
    re_path(r'^discard_course/(?P<enquiries_id>[\d]+)/$', csrf_exempt(views.discardCourse), name="discardCourse"),
    re_path(r'^course_content_send/(?P<pk>\d+)/enquiry/$', csrf_exempt(views.CoursesContentSendView.as_view()), name="CoursesContentSendView"),
    re_path(r'^send_account_details_send/(?P<pk>\d+)/enquiry/$', csrf_exempt(views.AccountDetailSendView.as_view()), name="accountdetailsendview"),

    path('edz', views.eduzillacomment, name="enquiry"),
    path('', csrf_exempt(views.enquiry), name="enquiry"),
    path("download_excel",views.download_excel,name="download_excel"),
    path("download_pdf",views.download_pdf,name="download_pdf"),
    path("get_enquirie_details",views.get_enquirie_details,name="get_enquirie_details"),
    path("mark-as-junk",views.mark_as_junk,name="mark_as_junk"),
    path("mark-as-real",views.mark_as_real,name="mark_as_real"),
    path("send-introduction-email",views.send_introduction_email,name="send_introduction_email"),
    path("add_enquiry_modal",views.add_enquiry_modal,name="add_enquiry_modal"),
    path("get_unattended_enq",views.get_unattended_enq,name="get_unattended_enq"),
]
