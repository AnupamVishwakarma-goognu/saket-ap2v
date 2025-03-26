from django.urls import path, re_path
from .import views

urlpatterns = [
    path('add_course_to_cart', views.add_course_to_cart, name="add_course_to_cart"),
    path('get_user_cart_count', views.get_user_cart_count, name="get_user_cart_count"),
    path('add_choice_to_cart', views.add_choice_to_cart, name="add_choice_to_cart"),
    path('show_hide_model', views.show_hide_model, name="show_hide_model"),
    path('language_add_batch', views.language_add_batch, name="language_add_batch"),
        
]