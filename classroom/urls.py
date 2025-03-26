# from django.conf.urls import url
from django.urls import path
from classroom import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('attemptuserLogin/', views.attemptuserLogin, name="attemptuserLogin"),
    path('logout', views.logout, name="logout"),
    path('signup', views.signup, name="signup"),

    path('playback/<str:class_link>', views.playback, name='playback'),


    # path('classroomhome', views.classroomhome, name="classroomhome"),
    path('get_study_materials/', views.get_study_materials, name='get_study_materials'),

    path('', views.classroom, name='classroom'),
    path('course-materials/<str:active_link>', views.course_materials, name='course_materials'),
    path('curriculum/<str:active_link>', views.curriculum, name='curriculum'),
    path('feedback/<str:active_link>', views.feedback, name='feedback'),
    path('system-requirements/', views.system_requirements, name='system-requirements'),
    
    path('get_recording', views.get_recording, name='get_recording'),
    path('download_certificate/<slug:batch_name>/<slug:slug>', views.download_certificate, name='download_certificate'),

    path('play/<int:composite_id>/<int:user>', views.recording_play, name='recording_play'),
    path('classplay/<str:class_link>', views.class_recording_play, name='class_recording_play'),
    path('class_recording/<str:class_link>', views.class_recording_play, name='class_recording_play'),
    path('class_recording_demo/<str:class_link>', views.class_recording_demo_play, name='class_recording_demo_play'),
    path('recording/<int:composite_id>/<int:user>', views.recording_play, name='recording_play'),

    path('get_batch_student_details/', views.get_batch_student_details, name='get_batch_student_details'),

    path('calender', views.calender, name='calender'),
    path('get_calender_day_event/', views.get_calender_day_event, name='get_calender_day_event'),
    path('submitStudentFeeback/', views.submitStudentFeeback, name='submitStudentFeeback'),
    
    path('certificate/<slug:slug>', views.genrate_certificate, name='genrate_certificate'),
    path('mark_stu_attendance', views.mark_stu_attendance, name='mark_stu_attendance'),
    path('get_batch_student_attendance_details/', views.get_batch_student_attendance_details, name='get_batch_student_attendance_details'),
    path('mark_joined', views.mark_joined, name='mark_joined'),
    path('mark-batch-as-completed-by-instructor', views.mark_batch_as_completed_by_instructor, name='mark_batch_as_completed_by_instructor'),
    path('play-back',views.demo_play,name="demo_play"),
    path('start-batch', views.start_batch, name='start_batch'),
    path('getting_meeting_details_student', views.getting_student_batch_details, name='getting_student_batch_details'),


    path('join-batch', views.join_batch, name='join_batch'),
    path('join-batch-test', views.join_batch_test, name='join_batch_test'),
    
    path('getting_meeting_details', views.getting_meeting_details, name='getting_meeting_details'),
    path('getting_meeting_details_test', views.getting_meeting_details_test, name='getting_meeting_details_test'),
    path('get_recording_left_side', views.get_recording_left_side, name='get_recording_left_side'),
    path('recording_buy', views.recording_buy, name="recording_buy"),
    path('paymentSuccess', views.paymentSuccess, name="paymentSuccess"),
    path('availCourse', views.availCourse, name="availCourse"),
    
    
    
]
