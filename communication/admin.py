from django.contrib import admin

# Register your models here.
from .models import CounselorContactNumber
class CounselorContactNumberAdmin(admin.ModelAdmin):
    list_display =['id','name','number','used_number']
admin.site.register(CounselorContactNumber,CounselorContactNumberAdmin)
