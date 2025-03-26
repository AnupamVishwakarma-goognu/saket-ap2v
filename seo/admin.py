from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Meta)

class SkillsContentAdmin(admin.ModelAdmin):
    list_display = ['id','uri']
admin.site.register(SkillsContent,SkillsContentAdmin)
