from django.urls import path, re_path
from .import views


urlpatterns = [
    path("drop_student/",views.drop_student,name="drop_student"),
    path("rejoin_student/",views.rejoin_student,name="rejoin_student"),
    path("refund_payment/",views.refund_payment,name="refund_payment"),
    path("shared_book_add/",views.shared_book_add,name="shared_book_add"),
    path('paid2/',views.paidInstallment2, name="paidInstallment2"),
    path("partner_payment_add/", views.partner_payment_add, name="partner_payment_add"),
    path("partner_payment_update/", views.partner_payment_update, name="partner_payment_update"),
    path('update_enrolment/',views.update_enrolment, name="update_enrolment"),
    # re_path('installment/(?P<enrollment_id>[\w]+)/$', views.installment, name="installment"),
    # re_path('installment/list/', views.list_installment, name= "list_installment"),
    re_path(r'^todo_installment/$', views.TodoInstallmentTemplateView.as_view(), name="TodoInstallmentTemplateView"),
    re_path(r'^view/installment/(?P<pk>\d+)/$', views.ViewInstallmentTemplateView.as_view(), name="ViewInstallmentTemplateView"),
    re_path('^$', views.enrollmentList, name="list"),
    re_path(r'^(?P<enquiryid>[\w]+)/$', views.enrollment, name="enrollment"),
    re_path('view/(?P<enrollment_id>[\w]+)/$', views.enrollsview, name="enrollment_view"),
    # re_path('paid/(?P<paid_id>[\d]+)/$', views.paidInstallment, name="paidInstallment"),
    re_path('search', views.enroll_search, name="enroll_search"),
    re_path('fees', views.fees_view, name="fees_list"),
    path("save_enroll_data", views.save_enroll_data, name="save_enroll_data"),
    path("update_partnet_data", views.update_partnet_data_section, name="update_partnet_data"),    

    path("download_excel",views.download_excel,name="download_excel"),
    path("download_pdf",views.download_pdf,name="download_pdf"),
    path("update_book",views.update_book,name="update_book"),
    path("save_attachment",views.save_attachment,name="save_attachment"),
    path("enrollmentsCSV",views.enrollmentsCSV,name="enrollmentsCSV"),
    path("send_enroll_mail_again",views.send_enroll_mail_again,name="send_enroll_mail_again"),
    path("check-student-enrolled-batches",views.check_student_enrolled_batches,name="check_student_enrolled_batches"),

    path("create-revision-enrollment",views.create_revision_enrollment,name="create_revision_enrollment")
    
    
    
]
