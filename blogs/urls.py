# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.all_blogs, name="blogs-list"),
    path('', views.listing, name="blogs"),
    path('subscribenewslatter', views.subscribenewslatter, name="subscribenewslatter"),
    path('blog-in-<slug:slug>', views.listing_city_blog, name="listing_city_blog"),
    path('<slug:slug>', views.display, name="blogs_display"),
    path('category/<slug:slug>', views.category, name="category"),
    path('tags/<slug:slug>', views.tags_blog, name="tags"),
    # path('<slug:slug>', views.display_blog, name="blogs"),
]
