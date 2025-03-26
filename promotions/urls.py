from django.urls import path, re_path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('view-template/<slug:name>',views.view_template,name="view_template"),
    
    path('', views.list_promotions, name="list_promotions"),
    path('add_promotion/',views.add_promotion,name="add_promotion"),
    path('get_campaign_template',views.get_campaign_template,name="get_campaign_template"),
    path('get_template_type',views.get_template_type,name="get_template_type"),
    
    path('display_campaign_view',views.display_campaign_view,name="display_campaign_view"),
    path('send_mails',views.send_mails,name="send_mails"),
    path('send-html-mails',views.send_html_mails,name="send_html_mails"),

    path('check_upload_csv',views.check_upload_csv,name="check_upload_csv"),
    path('download-report/<int:id>',views.download_report,name="download_report"),

    


    # path('test_email',views.test_email,name="test_email"),

]
