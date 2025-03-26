from django.urls import path
from .import views


urlpatterns = [
    path('get_counselor_round_number', views.get_counselor_round_number, name="get_counselor_round_number"),
    path('get_country_ip_loc', views.get_country_ip_loc, name="get_country_ip_loc"),
    path('validate-auth-token',views.validate_auth_token, name="validate_auth_token"),
    path('url-cache-script-logs',views.url_cache_script_logs, name="url_cache_script_logs"),

]
