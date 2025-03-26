from platform import platform
from django.db import models
from users.models import CustomUserModel as User
import uuid

# Create your models here.
class SEOBaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    breadcrumb = models.CharField(max_length=200, null=False, blank=False, default="Breadcrumb")
    title = models.CharField(max_length=200, null=True, blank=True, default="Page Title")
    meta_keyword = models.TextField(null=True, blank=True,)
    meta_description = models.TextField(null=True, blank=True,)
    gplus_headers = models.BooleanField(default=True) 
    twitter_headers = models.BooleanField(default=True)
    fb_og_headers = models.BooleanField(default=True)

    def __str__(self):
        value = self.title if hasattr(self,'title') else getattr(self,"id")
        return "{}".format(value)

    class Meta:
        abstract = True

class Image(models.Model):
    image = models.FileField(upload_to = "", null=True, blank=True)
    hash_value = models.CharField(max_length = 250, null=True, blank=True)

class BatchRecordingsURL(models.Model):
    BATCH_TYPE = (
        ('1', 'Batch'),
        ('2', 'Demo-Batch'),
        )
    # PLATFORM = (
    #     ('1', 'Blue-Jeans'),
    #     ('2', 'Zoom'),
    #     )
    # recording_platform = models.CharField(max_length=2,choices=PLATFORM,default=None)
    batch = models.CharField(max_length=2,choices=BATCH_TYPE,default=None)
    meeting_id = models.CharField(max_length=100,null=True, blank=True)
    composite_id = models.CharField(max_length=100,null=True, blank=True)
    recording_on = models.DateTimeField(null=True,blank=True)
    link = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    download = models.BooleanField(default=False, null=True, blank=True)
    upload = models.BooleanField(default=False, null=True, blank=True)
    duration = models.CharField(max_length=100,null=True, blank=True,default='0')

class RecordingProcessDate(models.Model):
    date = models.DateField(auto_now_add=True)

class CommanModal(models.Model):
    last_recording_url_count = models.IntegerField(default=0,null=True,blank=True)

class OfferEndDate(models.Model):
    added_on = models.DateField(auto_now_add=True)
    offer_end_date = models.DateField(null=True, blank=True)
    offer_text = models.CharField(max_length=100, help_text="Text cannot be grater then 80 character",null=True, blank=True)

class CountryCode(models.Model):
    country = models.CharField(null=False,blank=False, max_length=250)
    country_code = models.CharField(null=False,blank=False, max_length=50)
    dialing_code = models.CharField(null=False,blank=False, max_length=100)

class ZoomRecordingURL(models.Model):
    BATCH_TYPE = (
        ('1', 'Batch'),
        ('2', 'Demo-Batch'),
        )
    
    batch = models.CharField(max_length=2,choices=BATCH_TYPE,default=None)
    meeting_id = models.CharField(max_length=100,null=True, blank=True)
    composite_uuid_id = models.CharField(max_length=250,null=True, blank=True)
    recording_on = models.DateTimeField(null=True,blank=True)
    link = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    download = models.BooleanField(default=False, null=True, blank=True)
    upload = models.BooleanField(default=False, null=True, blank=True)
    duration = models.CharField(max_length=100,null=True, blank=True,default='0')


class AuthToken(models.Model):
    added_on = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    token =  models.UUIDField(default=uuid.uuid4, null=False, blank=False, unique=True)

    # def save(self, *args, **kwargs):
    #     if not self.token:
    #         super(AuthToken, self).save(*args, **kwargs)



class UrlCacheScriptLog(models.Model):
    added_on = models.DateTimeField(auto_now_add = True)
    start_script = models.BooleanField(null=True, blank= True, default=False)
    log_file = models.FileField(upload_to="url_cache_script_log", null=True, blank=True)
    complete_script = models.BooleanField(null=True, blank= True, default=False)
    complete_on = models.DateTimeField(null=True, blank= True, default=None)