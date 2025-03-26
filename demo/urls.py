from django.urls import path
from .import views


urlpatterns = [
    path('',views.demoList, name="demoList"),
    path('get_enquiry_student',views.get_enquiry_student, name="get_enquiry_student"),
    path('get_student_name',views.get_student_name, name="get_student_name"),
    path('create_demo_batch',views.create_demo_batch,name="create_demo_batch"),
    path('get_batch_student',views.get_batch_student,name="get_batch_student"),
    path('get_smsTemplate',views.get_smsTemplate,name="get_smsTemplate"),
    path('delete_batch',views.delete_batch,name="delete_batch"),
    path('add_more_student',views.add_more_student,name="add_more_student"),
    path('demoVideo',views.demoVideo,name="demoVideo"),
    path('demoSave',views.demoSave,name="demoSave"),
    

    path('join-demo/<uuid:uuid>',views.student_waiting_page,name="waiting"),
    path('student-check-for-demo-start', views.student_check_for_demo_start,name="student_check_for_demo_start"),

    path('waiting-to-start-demo/<uuid:uuid>', views.waiting_to_start_demo,name="waiting_to_start_demo"),
    path('create-demo-sesion-zoom-meeting-id', views.create_demo_sesion_zoom_meeting_id,name="create_demo_sesion_zoom_meeting_id"),

    # path('waiting/<uuid:uuid>',views.waiting_page_for_student,name="waiting_page_for_student"),
    # path('waiting-to-join-demo',views.waiting_to_join_demo,name="waiting_to_join_demo"),


    # path('waiting-to-start-demo',views.waiting_to_start_demo,name="waiting_to_start_demo")
    # path('creating-demo-inst',views.creating_demo_inst,name="creating_demo_inst")
]
