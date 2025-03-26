from django.urls import path
from . import views

urlpatterns = [
    #path('offers/', views.offers),--------------------------Don't uncommnt--------------------
    path('contact-old/', views.contact_us, name="contact-us"),
    #path('online-courses-old/', views.online_courses, name="training_online"),
    path('about-us/', views.about_us, name="about-us"),
    path('refer-earn/', views.refer_and_earn, name="refer_and_earn"),
    path('refer-earn-register/', views.refer_earn_register, name="refer-earn-register"),
    path('thankyou/', views.thankyou, name="thankyou"),
    path('why-ap2v/', views.whyap2v, name="whyap2v"),
    path('add-enquiry/', views.add_enquiry, name="add-enquiry"),
    path('send-enquiry/', views.send_enquiry, name="send-enquiry"),
    path('contact-popup-enquiry/', views.contact_enquiry, name="contact-popup-enquiry"),
    path('call-popup-enquiry/', views.call_enquiry, name="call-popup-enquiry"),
    # path('', views.home, name="home"),--------------------------Don't uncommnt--------------------
    path('', views.home, name="home"),
    path('contact-popup-enquiry-down/', views.contact_enquiry_down, name="contact-popup-enquiry-down"),
    path('contact-popup-enquiry-call/', views.contact_enquiry_call, name="contact-popup-enquiry-call"),
    path('popup_session', views.PopUPSessionView.as_view(), name="PopUPSessionView"),

    path('contact-us/', views.contact_us, name="contact-us"),
    path('about-us/', views.about_us, name="about-us"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions/', views.terms_and_conditions, name="terms-and-conditions"),
    # path('city-sitemap/', views.city_sitemap, name="city-sitemap"),
    # path('400/',views.error400, name='400error'),
    # path('500/',views.error500, name='500error'),
    path('city-sitemap/', views.city_sitemap, name="city-sitemap"),
    path('city-sitemap/<slug:city>', views.city_sitemap_category, name="city_sitemap_category"),
    path('sitemap/', views.sitemap, name="sitemap"),
    path('5xx/', views.error_5xx, name="error-5xx"),
    path('4xx/', views.error_4xx, name="error-4xx"),
    path('create_enquiry', views.create_enquiry, name="create_enquiry"),
    path('find',views.find, name="find"),                                   #API for search instant response 
    path('search',views.search, name="search"),
    path('verify/',views.verify, name="verify"),
]
