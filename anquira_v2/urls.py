from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage-admin/', admin.site.urls),
    path('followups/', include('followups.urls')),
    path('dashboard/', include('website.urls')),
    path('enquiries/', include('enquiries.urls')),
    path('courses/', include('courses.urls')),
    path('batches/', include('batches.urls')),
    path('instructors/', include('instructors.urls')),
    path('enrollments/', include('enrolls.urls')),
    path('promotions/', include('promotions.urls')),
    path('api/', include('enquiries.api_urls')),
    path('activity/', include('activity.urls')),
    path('bluejeans/', include('bluejeans.urls')),
    path('demo/',include('demo.urls')),
    path('report/',include('reporting.urls')),
    path('payment/',include('payment.urls')),
    path('feedback/',include('feedback.urls')),
    path('logs/',include('core.urls')),

    path('ckeditor',include('ckeditor_uploader.urls')),
    

    path('', include('users.urls')),
    path('recording_sessions/',include('recording_sessions.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
