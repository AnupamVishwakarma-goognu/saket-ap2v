from sunau import AUDIO_FILE_MAGIC
from django.contrib import admin
from.models import Recorded_Courses_name,OnlineBuyedCourse, Recorded_Uploading_S3_Logs,Purchased_classroom_recording_course,Order,temp_recored_detail,temp_order_detail
# Register your models here.
class RecordingCourseAdmin(admin.ModelAdmin):
    list_display=['id','course','status','number']
admin.site.register(Recorded_Courses_name,RecordingCourseAdmin)

class RecordingUploadAdmin(admin.ModelAdmin):
    list_display=['id','course_name','name','date','status']
admin.site.register(Recorded_Uploading_S3_Logs,RecordingUploadAdmin)

class PurchasedAdmin(admin.ModelAdmin):
    list_display=['id','user','course_name','date']
admin.site.register(Purchased_classroom_recording_course,PurchasedAdmin)

class TemprecAdmin(admin.ModelAdmin):
    list_display=['id','user','course','price', 'email', 'date']
admin.site.register(temp_recored_detail,TemprecAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','amount','payment_id','status']
admin.site.register(Order,OrderAdmin)

class temp_order_detailAdmin(admin.ModelAdmin):
    list_display=['id','user_name','order_id',]
admin.site.register(temp_order_detail,temp_order_detailAdmin)

class OnlineBuyedCourseAdmin(admin.ModelAdmin):
    list_display=['id','user_id','course','course_type','date']
admin.site.register(OnlineBuyedCourse,OnlineBuyedCourseAdmin)