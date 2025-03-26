from django.contrib import admin
from .models import *

# Register your models here.


class Learning_PathAdmin(admin.ModelAdmin):
    list_display = ['pk','slug','heading','description','preview_video_link','banner_image']
admin.site.register(Learning_Path,Learning_PathAdmin)


class Learning_PathAdmin(admin.ModelAdmin):
    list_display = ['pk', 'index','courses', 'learning_path']
admin.site.register(Learning_Path_Courses, Learning_PathAdmin)

class City_Specific_Learning_PathAdmin(admin.ModelAdmin):
    list_display = ['pk', 'parent_learning_path','slug','heading','description','city','show_tranding_in_footer']
admin.site.register(City_Specific_Learning_Path,City_Specific_Learning_PathAdmin)


#class City_Specific_Learning_Path_CoursesAdmin(admin.ModelAdmin):
#    list_display = ['pk', 'index','courses', 'learning_path']
#admin.site.register(City_Specific_Learning_Path_Courses,City_Specific_Learning_Path_CoursesAdmin)
