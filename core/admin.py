from django.contrib import admin

# Register your models here.

from .models import Image
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','image','hash_value']
admin.site.register(Image,ImageAdmin)

from .models import BatchRecordingsURL
class BatchRecordingsURLAdmin(admin.ModelAdmin):
    list_display = ['id','batch','meeting_id','composite_id','link','date','download','upload','duration']
admin.site.register(BatchRecordingsURL,BatchRecordingsURLAdmin)

from .models import RecordingProcessDate
class RecordingProcessDateAdmin(admin.ModelAdmin):
    list_display = ['id','date']
admin.site.register(RecordingProcessDate,RecordingProcessDateAdmin)

from .models import CommanModal
class CommanModalAdmin(admin.ModelAdmin):
    list_display = ['id','last_recording_url_count']
admin.site.register(CommanModal,CommanModalAdmin)

from .models import OfferEndDate
class OfferEndDateAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','offer_end_date']
admin.site.register(OfferEndDate,OfferEndDateAdmin)

from .models import CountryCode
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ['id','country','country_code','dialing_code']
admin.site.register(CountryCode,CountryCodeAdmin)

from .models import ZoomRecordingURL
class ZoomRecordingURLAdmin(admin.ModelAdmin):
    list_display = ['id','batch','meeting_id','composite_uuid_id','recording_on','date','download','upload','duration']
admin.site.register(ZoomRecordingURL,ZoomRecordingURLAdmin)


from .models import AuthToken
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','user','token']
    readonly_fields = ['token']
admin.site.register(AuthToken, AuthTokenAdmin)


from .models import UrlCacheScriptLog
class UrlCacheScriptLogAdmin(admin.ModelAdmin):
    list_display = ['id','added_on','start_script','complete_script','log_file']
admin.site.register(UrlCacheScriptLog,UrlCacheScriptLogAdmin)