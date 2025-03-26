from django.contrib import admin
from .models import *

# Register your models here.


class TextAdmin(admin.ModelAdmin):
    list_display = ['id','course','name','designation','company','rating','date','image','tags']
admin.site.register(Text,TextAdmin)
admin.site.register(Video)
