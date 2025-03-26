from django.contrib import admin

# Register your models here.
from .models import AccessToken
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ['id','access_token','user','enterprise']
admin.site.register(AccessToken,AccessTokenAdmin)