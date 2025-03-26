from django.contrib import admin

# Register your models here.
from .models import ChatFile
class ChatFileAdmin(admin.ModelAdmin):
    list_display=['id','file','batch','current_batch_id_forward']
admin.site.register(ChatFile,ChatFileAdmin)