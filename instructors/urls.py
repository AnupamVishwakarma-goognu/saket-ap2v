from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.instructor, name="instructor"),
    path('list/', views.instructorlist, name="instructorlist"),
    path('list/inactive', views.inactive_instructorlist, name="inactive_instructorlist"),
    re_path(r'^view/(?P<instructors_id>[\w]+)/$', views.instructorview, name="instructorview"),
    re_path(r'^(?P<pk>\d+)/delete/$', views.InstructorsDeleteView.as_view(), name="InstructorsDeleteView"),
    re_path(r'^(?P<instructor_id>\d+)/update/$', views.InstructorupdateView.as_view(), name="InstructorupdateView"),
    path('get_instructors_course', views.get_instructors_course, name="get_instructors_course"),

    path('mark-active-inst', views.mark_as_instructore,name="mark_as_instructore"),
    path('genrate_zoom_user/<int:user_id>', views.genrate_zoom_user,name="genrate_zoom_user"),
    path('use_comman_zoom_user/<int:user_id>', views.use_comman_zoom_user,name="use_comman_zoom_user"),
    path('target-record', views.target_record,name="target_record"),
    path('counselor-record', views.counselor_record,name="counselor_record"),
    path('all-couselor-record', views.all_couselor_record,name="all_couselor_record"),
]
