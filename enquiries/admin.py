from django.contrib import admin
from .models import *

#admin.site.register(TimePrefer)

class EnquiriesAdmin(admin.ModelAdmin):
    list_display = ['id','junk','attended','full_name','email','mobile','courses','assigned_by','added_on','update_on']
    search_fields=['full_name','added_on']
    list_display_links=['id','full_name','email']
    list_filter = ['added_on','junk']
admin.site.register(Enquiries,EnquiriesAdmin)
#admin.site.register(Reference)

class FollowupsAdmin(admin.ModelAdmin):
    list_display = ['id','followupid','followup_mode','response','next_followup','comments','status','is_complete','assigned_user','added_on']
    list_filter = ['added_on']
admin.site.register(Followups,FollowupsAdmin)

class EnquiryCoursesAdmin(admin.ModelAdmin):
    list_display = ['id','enquiry_id','courses','status','comment','tmp_discard','enroll','added_on']
admin.site.register(EnquiryCourses,EnquiryCoursesAdmin)

admin.site.register(InformationSharingTemplate)
admin.site.register(StudentResponse)

from .models import ReassignedEnquiryLogs
class ReassignedEnquiryLogsAdmin(admin.ModelAdmin):
    list_display = ['id','enquiry','from_counselor','to_counselor','assigned_on']
admin.site.register(ReassignedEnquiryLogs,ReassignedEnquiryLogsAdmin)