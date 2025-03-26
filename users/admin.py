from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display =['id','first_name','email','username','user_type','exist_employee','mobile','location','is_verified','is_staff','is_superuser']
    
    # def save_model(self, request, obj, form, change):
    #     # Override this to set the password to the value in the field if it's
    #     # changed.
    #     if obj.pk:
    #         orig_obj = CustomUserModel.objects.get(pk=obj.pk)
    #         if obj.password != orig_obj.password:
    #             obj.set_password(obj.password)
    #     else:
    #         obj.set_password(obj.password)
    #     obj.save()


# admin.site.register(CustomUserModel,UserAdmin)
# admin.site.register(CustomUserModel)


# @admin.register(CustomUserModel)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Custom Fields', {'fields': ('location', 'user_type', 'exist_employee', 'is_verified')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'location', 'user_type', 'exist_employee', 'is_verified'),
#         }),
#     )
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type', 'location')
#     search_fields = ('username', 'first_name', 'last_name', 'email')
#     ordering = ('username',)
admin.site.register(CustomUserModel)
from .models import CounselorPreferences
class CounselorPreferencesAdmin(admin.ModelAdmin):
    list_display = ['id','user','last_assigned']
admin.site.register(CounselorPreferences,CounselorPreferencesAdmin)


from .models import PartnerPreferences
class PartnerPreferencesAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(PartnerPreferences,PartnerPreferencesAdmin)

from .models import UserRegistrationVerification
class UserRegistrationVerificationAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','added_on','token','uuid']
admin.site.register(UserRegistrationVerification,UserRegistrationVerificationAdmin)

from .models import UserPasswordResetVerification
class UserPasswordResetVerificationAdmin(admin.ModelAdmin):
    list_display = ['id','email','token','uuid','date']
admin.site.register(UserPasswordResetVerification,UserPasswordResetVerificationAdmin)

from .models import CertificateId
class CertificateIdAdmin(admin.ModelAdmin):
    list_display = ['cert_id','user']
admin.site.register(CertificateId,CertificateIdAdmin)