# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('load-course-content/', views.load_course_content,name="load_course_content"),
    path('load-course-content-full/', views.load_course_content_full,name="load_course_content_full"),
    path('certifications/', views.certifications),
    path('contact-popup-enquiry-down/', views.contact_enquiry_down, name="contact-popup-enquiry-down"),
    path('contact-popup-enquiry-call/', views.contact_enquiry_call, name="contact-popup-enquiry-call"),
    path('contact-popup-enquiry/', views.contact_enquiry, name="contact-popup-enquiry"),
    path('enquirysave/', views.enquirysave),
    #path('<slug:slug>/', views.landing_page),
    #path('<slug:slug>', views.landing_page),
]
