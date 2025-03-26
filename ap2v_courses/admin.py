from django.contrib import admin

from .models import *
# Register your models here.


class CoursesAdmin(admin.ModelAdmin):
    list_display = ['id','active_inactive','name','slug','duration','course_icon','price','actual_price']
admin.site.register(Courses,CoursesAdmin)

class City_Specific_CourseAdmin(admin.ModelAdmin):
    list_display = ['name','active_inactive','course','slugs','city','show_tranding_in_footer']
    
admin.site.register(City_Specific_Course,City_Specific_CourseAdmin)

class Courses_QnAAdmin(admin.ModelAdmin):
    list_display =['id','course','question']
admin.site.register(Courses_QnA,Courses_QnAAdmin)

class OffersAdmin(admin.ModelAdmin):
    list_display = ['id','title','added_on','price','valid_till']
admin.site.register(Offers,OffersAdmin)

class LessonsAdmin(admin.ModelAdmin):
    list_display = ['id','course','name','duration','requirments']
admin.site.register(Lessons,LessonsAdmin)

admin.site.register(Locations)

class RemoteItemsAdmin(admin.ModelAdmin):
    list_display = ['id','title','link','location']
admin.site.register(RemoteItems,RemoteItemsAdmin)

class Industry_ProjectsAdmin(admin.ModelAdmin):
    list_display = ['id','belong_course','heading','description']
admin.site.register(Industry_Projects,Industry_ProjectsAdmin)

class Course_FQAAdmin(admin.ModelAdmin):
    list_display = ['id','belong_course','frequently_question']
admin.site.register(Course_FQA,Course_FQAAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','breadcrumb','image']
admin.site.register(City,CityAdmin)

from .models import CitySpecificCoursesFQA
class CitySpecificCoursesFQAAdmin(admin.ModelAdmin):
    list_display = ['id','belong_city_spqcific_course','frequently_question']
admin.site.register(CitySpecificCoursesFQA,CitySpecificCoursesFQAAdmin)


from .models import OnlineContentRelatedCourse
class OnlineContentRelatedCourseAdmin(admin.ModelAdmin):
    list_display = ['id','course','get_content_related_online_courses','get_content_related_city_courses']
    
    def get_content_related_online_courses(self, obj):
        if obj.content_related_online_courses.all():
            return list(obj.content_related_online_courses.all().values_list('name', flat=True))
        else:
            return 'NA'
    def get_content_related_city_courses(self, obj):
        if obj.content_related_city_courses.all():
            return list(obj.content_related_city_courses.all().values_list('name', flat=True))
        else:
            return 'NA'
admin.site.register(OnlineContentRelatedCourse,OnlineContentRelatedCourseAdmin)

from .models import CityContentRelatedCourse
class CityContentRelatedCourseAdmin(admin.ModelAdmin):
    list_display = ['id','city_course','get_content_related_online_courses','get_content_related_city_courses']
    
    def get_content_related_online_courses(self, obj):
        if obj.content_related_online_courses.all():
            return list(obj.content_related_online_courses.all().values_list('name', flat=True))
        else:
            return 'NA'
    def get_content_related_city_courses(self, obj):
        if obj.content_related_city_courses.all():
            return list(obj.content_related_city_courses.all().values_list('name', flat=True))
        else:
            return 'NA'
admin.site.register(CityContentRelatedCourse,CityContentRelatedCourseAdmin)