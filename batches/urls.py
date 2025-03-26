from django.urls import path, re_path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    re_path('^$', views.batches, name="batches"),
    re_path('list/$', views.batchlist, name="batchlist"),
    re_path('view/(?P<batches_id>[\w]+)/$', views.batchView, name='batchView'),
    re_path(r'^(?P<batch_id>\d+)/update/$', csrf_exempt(views.BatchupdateView.as_view()), name="BatchupdateView"),
    path('get_filter_student',views.get_filter_student , name="get_filter_student"),
    path('get_course_student',views.get_course_student , name="get_course_student"),
    path('get_student_name',views.get_student_name , name="get_student_name"),
    path('removeStudentFromBatch',views.removeStudentFromBatch , name="removeStudentFromBatch"),
    path('update_batch',views.update_batch , name="update_batch"),
    path('get_batch_recording',views.get_batch_recording , name="get_batch_recording"),
    path('batch_calender',views.batch_calender , name="batch_calender"),

    path('get_recording_for_anquira', views.get_recording_for_anquira, name='get_recording_for_anquira'),
    path('mark_recording', views.mark_recording, name='mark_recording'),
    path('marked_recording', views.marked_recording, name='marked_recording'),
    path('removeMarkedRecording', views.removeMarkedRecording, name='removeMarkedRecording'),
    path('get_batch_attendance', views.get_batch_attendance, name='get_batch_attendance'),
    path('add-batch-session-off-date', views.add_batch_session_off_date, name='add_batch_session_off_date'),
    path('batch-progress', views.batch_progress, name='batch_progress'),
    path('get-batch-progress-data', views.get_batch_progress_data, name='get_batch_progress_data'),
    path('batch-public-holiday', views.batch_public_holiday, name='batch_public_holiday'),
    path('add-batch-public-holiday', views.add_batch_public_holiday, name='add_batch_public_holiday'),

    path('add-zoom-weebhook-response', views.add_zoom_weebhook_response, name="add_zoom_weebhook_response"),
    path('get_end_date',views.get_end_date,name="get_end_date")
    

]
