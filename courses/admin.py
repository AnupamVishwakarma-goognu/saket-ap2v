from django.contrib import admin
from .models import *

class CoursesAdmin(admin.ModelAdmin):
    list_display = ['id','name','url','price','course_content','is_exam','original_price']
admin.site.register(Courses,CoursesAdmin)

class BooksAdmin(admin.ModelAdmin):
    list_display = ['id','name','course','cost','added_on','stock']
admin.site.register(Books,BooksAdmin)

admin.site.register(Exams)