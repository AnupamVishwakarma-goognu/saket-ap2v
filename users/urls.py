from django.urls import path, re_path
from .import views

urlpatterns = [
    re_path('^$', views.llogin, name="login"),
    path('authlogin/', views.users, name="user"),
    path('logout/', views.logout, name="logout"),
    path('edit-profile/', views.edit_profile, name="editprofile"),
    path('create_user/',views.create_user,name="create_user"),
    path('activate/<str:token>/<slug:uuid_gen>',views.activate,name="activate"),
    path('genrate_reset_user_password_token',views.genrate_reset_user_password_token, name="genrate_reset_user_password_token"),
    path('reset_password', views.reset_password, name="reset_password"),
    path('reset/<str:token>/<slug:uuid_gen>',views.reset_password_link_validate,name="reset_password_link_validate"),
    path('verify/<str:token>/<slug:uuid_gen>',views.auto_reg_activate,name="auto_reg_activate"), #use for verify user which is auto genrate user while enrolling student

]
