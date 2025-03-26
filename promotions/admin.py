from django.contrib import admin

# Register your models here.

from .models import CampaignTemplate, Campaign

class CampaignTemplateAdmin(admin.ModelAdmin):
    list_display = ['id','camp_temp_type','template_name','template_text','variable_count']
admin.site.register(CampaignTemplate,CampaignTemplateAdmin)

class CampaignAdmin(admin.ModelAdmin):
    list_display = ['id','campaign_template','date','source','location','approved','complate','start_triggered','c_type']
admin.site.register(Campaign,CampaignAdmin)


from .models import SendBulkMail
class SendBulkMailAdmin(admin.ModelAdmin):
    list_display = ['id','approved','date','target_user','template_name','is_complete','location']
admin.site.register(SendBulkMail,SendBulkMailAdmin)