from django.contrib import admin


from .models import Batches
class BatchesAdmin(admin.ModelAdmin):
    list_display = ['id','instructors','chat_room_id','start_date_time','end_date_time','complete','bitly_link_instructer','bitly_link_student_mobile','days_of_week','complete','zoom_bitly_link_instructer','zoom_bitly_link_student_mobile']
    list_display_links = ['id']
    list_filter = ['instructors','zoom_bitly_link_instructer','zoom_bitly_link_student_mobile']
admin.site.register(Batches,BatchesAdmin)


from .models import StudentCertificateIssued
class StudentCertificateIssuedAdmin(admin.ModelAdmin):
    list_display = ['id','name','course','date','code','uuid','user','batch','enroll']
    list_display_links = ['id','name']
    list_filter = ['batch','date']
admin.site.register(StudentCertificateIssued,StudentCertificateIssuedAdmin)

from .models import BestRecording
class BestRecordingAdmin(admin.ModelAdmin):
    list_display = ['id','create_on','user','type','link','batch_demo_id','batch_name']
admin.site.register(BestRecording,BestRecordingAdmin)

from .models import BatchSessionOff
class BatchSessionOffAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','batch','off_date']
admin.site.register(BatchSessionOff,BatchSessionOffAdmin)

from .models import UnsubscribeBatchReminderEmail
class UnsubscribeBatchReminderEmailAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','email']
admin.site.register(UnsubscribeBatchReminderEmail,UnsubscribeBatchReminderEmailAdmin)

from .models import PublicHoliday
class PublicHolidayAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','off_date','occasion']
admin.site.register(PublicHoliday,PublicHolidayAdmin)

from .models import ZoomMeetingIdUserBatch
class ZoomMeetingIdUserBatchAdmin(admin.ModelAdmin):
    list_display = ['id','meeting_type','date','batch','demo','meeting_id','meeting_status','meeting_start_at','meeting_end_at']
admin.site.register(ZoomMeetingIdUserBatch,ZoomMeetingIdUserBatchAdmin)

# from .models import ZoomMeetingIdUserDemo
# class ZoomMeetingIdUserDemoAdmin(admin.ModelAdmin):
#     list_display = ['id','date','demo','meeting_id','meeting_status','meeting_start_at','meeting_end_at']
# admin.site.register(ZoomMeetingIdUserDemo,ZoomMeetingIdUserDemoAdmin)

from .models import ZoomWeebHookResponce
class ZoomWeebHookResponceAdmin(admin.ModelAdmin):
    list_display = ['id','date','response']
admin.site.register(ZoomWeebHookResponce,ZoomWeebHookResponceAdmin)

from .models import ZoomLicenseDetails
class ZoomLicenseDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','total_license','use_license']
admin.site.register(ZoomLicenseDetails,ZoomLicenseDetailsAdmin)

from .models import CompleteRecording
class CompleteRecordingAdmin(admin.ModelAdmin):
    list_display = ['id','course','batch','date']
admin.site.register(CompleteRecording,CompleteRecordingAdmin)
