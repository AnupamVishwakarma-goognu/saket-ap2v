from django.contrib import admin
from .models import Instructors

class InstructorsAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','email','mobile','added_on','blue_jeans_user_id','blue_jeans_passcode','active']
admin.site.register(Instructors,InstructorsAdmin)
