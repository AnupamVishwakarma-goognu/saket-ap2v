"""ap2v URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.conf.urls import include, handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .import make_captcha
from django.contrib.sitemaps.views import sitemap
from sitemaps.views import CourseSitemap, CityCourseSitemap, LearningPathSitemap, CityLearningPathSitemap, StaticSitemap, CityTagSitemap, TagSitemap, CategorySitemap
from django.contrib.sitemaps import views as sitemaps_views
from ap2v_courses.views import all_courses as view_all_courses, landing_page as view_landing_page, all_coursesCity
from learning_paths.views import city_learning_paths
from ap2v_courses import views
from blogs.views import interview_questions_listing,interview_questions_display

admin.site.site_header = "AP2V Admin Panel"
admin.site.site_title = "AP2V Admin Dashboard"
admin.site.index_title = "Welcome to AP2V Dashboard"


sitemaps = {
    CourseSitemap.name: CourseSitemap,
    CityCourseSitemap.name: CityCourseSitemap,
    LearningPathSitemap.name: LearningPathSitemap,
    CityLearningPathSitemap.name: CityLearningPathSitemap,
    StaticSitemap.name: StaticSitemap,
    TagSitemap.name: TagSitemap,
    CityTagSitemap.name: CityTagSitemap,
    CategorySitemap.name: CategorySitemap
}


urlpatterns = [
    path('manage-admin/', admin.site.urls),
    path('core_apis/v1/',  include('core.urls')),
    path('e_store_apis/v1/',  include('ap2v_e_store.urls')),
    path('demo-session/',  include('demo.urls')),
    path('demo-class/',  include('classroom.urls')),
    path('pay',  include('payment.urls')),
    path('pay/',  include('payment.urls')),
    path('lp_enq/', include('ap2v_courses.urls'), name="landing-page"),
    path('login', include('social_django.urls', namespace='social')),
    #path('lp/', include('ap2v_courses.urls'), name="landing-page"),
    path('lp/<slug:slug>/', view_landing_page, name="landing-page"),
    path('events/', include('events.urls')),
    path('user/', include('users.urls')),
    path('blog/', include('blogs.urls')),
    path('interview-questions/', interview_questions_listing, name="interview-questions"),
    path('interview-questions/<slug:slug>', interview_questions_display, name="interview_questions_display"),
    path('learning-path/', include('learning_paths.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('category/<slug:category_slug>-in-<slug:city_slug>', views.display_category, name="display_city_category"),
    path('category/<slug:category_slug>', views.display_category, name="display_category"),
    path('<slug:tag>-courses-in-<slug:city_slug>', views.display_tag, name="display_city_tag"),
    path('<slug:tag>-courses', views.display_tag, name="display_tag"),
    path('offers/', views.offers, name="offers"),
    path('captcha', make_captcha.captcha_create, name="captcha"),
    #@@path('citysep/', include('ap2v_courses.urls'), name="citysep"),
    path('gallery/', include('gallery.urls'), name="gallery"),
    path('', include('home.urls')),
    # path('search', views.SearchFilterTemplateView.as_view(), name="SearchFilterTemplateView"),
    path('classroom/', include('classroom.urls')),
    path('classroom', include('classroom.urls')),
    path('chat/', include('django_chatter.urls')),
    path('chats/', include('chats.urls')),
    path('recording_sessions/',include('recording_sessions.urls')),
    path('cart/',include('recording_sessions.urls')),
    # path("error/",include('home.urls')),
    path('trending-courses/', views.trending_courses, name="trending-courses"),
    path('featured-courses/', views.featured_courses, name="featured-courses"),
    path('courses/', view_all_courses, name="course-listing"),
    path('courses-in-<slug:city_course>', all_coursesCity, name="course-listing_city"),
    path('learning-paths-in-<slug:city_lp>', city_learning_paths, name="city-learning-paths"),

    # path('', include('home.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.views.decorators.cache import cache_page

urlpatterns += [
    path('<slug:slug>', views.CoursesDynamicTemplateView.as_view(), name="course-detail"),
    #path('<slug:slug>/', views.CoursesDynamicTemplateView.as_view(), name="course-detail"),
    #path('<slug:slug>', cache_page(60*60)(views.CoursesDynamicTemplateView.as_view()), name="course-detail"),
]

urlpatterns += [
    path('sitemap.xml', sitemaps_views.index, {'sitemaps': sitemaps},
         name='sitemap-index'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]


handler404 = 'home.views.error_4xx'
handler500 = 'home.views.error_5xx'
