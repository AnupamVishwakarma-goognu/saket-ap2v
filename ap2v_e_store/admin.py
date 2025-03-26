from django.contrib import admin

# Register your models here.
from .models import CourseStoreCart
class CourseStoreCartAdmin(admin.ModelAdmin):
    list_display = ['id','date','user','course']
admin.site.register(CourseStoreCart,CourseStoreCartAdmin)