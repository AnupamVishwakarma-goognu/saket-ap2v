from django.contrib import admin

# Register your models here.
from .models import DemoSaveVideo
class DemoVideoAdmin(admin.ModelAdmin):
    list_display = ['id','course_name','file_name','added_on']
admin.site.register(DemoSaveVideo,DemoVideoAdmin)

from .models import DemoSMSTemplate
class DemoSMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['id','create_on','template_name','template_text','variable_count']
admin.site.register(DemoSMSTemplate,DemoSMSTemplateAdmin)


from .models import Demo
class DemoAdmin(admin.ModelAdmin):
    list_display = ['id','instructors','start_date_time','end_date_time','courses','bitly_link_instructer','bitly_link_student_mobile']
admin.site.register(Demo,DemoAdmin)

