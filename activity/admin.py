from django.contrib import admin

# Register your models here.

from .models import Activity
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id','user','typee','ref_type','add_on']
admin.site.register(Activity, ActivityAdmin)