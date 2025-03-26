from django.urls import path
from .import views

urlpatterns = [
    #path('', views.redirect, name="redirect"),
    #path('login/', views.login, name="login"),
    path('', views.dashboard, name="dashboard"),
    #path('authlogin/', views.authlogin, name="authlogin"),
    #path('logout/', views.logout, name="logout"),all-filter

    path('all-filter', views.all_filter, name="all_filter"),
    path('get_chart_data', views.get_chart_data, name="get_chart_data"),
    path('get_zoom_chart_data', views.get_zoom_chart_data, name="get_zoom_chart_data"),
]
