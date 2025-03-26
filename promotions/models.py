from django.core.exceptions import ValidationError
from django.db import models
import re
from django.db.models.fields import TextField

from django.http.response import HttpResponse
from communication.views import SendSMS,send_promotional_email
from ckeditor.fields import RichTextField
from django.conf import settings
from communication.views import send_bulk_email_comm


# from django.forms import ValidationError as FormValidationError

# Create your models here.

class CampaignTemplate(models.Model):
    CAMP_TEMP_TYPE =(
        ('1','Email'),
        ('2','SMS'),
    )
    camp_temp_type = models.CharField(max_length=15, choices=CAMP_TEMP_TYPE,null=False, blank=False, help_text="In SMS Message length cannot grater then 200 Char.")
    template_name = models.CharField(max_length=100, blank=True,null=True)
    template_text = RichTextField(help_text="use {} for veriable input.<b> Example: {course},{date}</b>")
    variable_count = models.IntegerField(blank=True,null=True, help_text="Leave blank this field")

    def __str__(self):
        return self.template_name

    def save(self):
        count = len(re.findall(r'{(.*?)}', self.template_text))

        self.variable_count = count

        if self.camp_temp_type=="2":
            cleaner = re.compile('<.*?>')
            string = re.sub(cleaner, '', self.template_text)
            string = string.replace("&nbsp;"," ")
            string = string.replace("&bull;"," ")

            len_string = len(string)
            if len_string > settings.SMS_CHAR_LIMIT:
                raise ValidationError("Validation Error")
                # return HttpResponse("Message length is grater then 200.")
            self.template_text = string
            
        super(CampaignTemplate, self).save()

class Campaign(models.Model):

    CAMP_TYPE =(
        ('0','Not Defined'),
        ('1','Email'),
        ('2','SMS'),
    )

    campaign_template = models.ForeignKey(CampaignTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    c_type = models.CharField(max_length=15, choices=CAMP_TYPE,default=2)
    source = models.CharField(max_length=15, blank=True,null=True)
    location = models.FileField(upload_to="campaign", blank=True,null=True)
    target_user = models.IntegerField(blank=True,null=True)
    send_to = models.IntegerField(blank=True,null=True)
    complate = models.BooleanField(default=False,blank=True,null=True)
    approved = models.BooleanField(default=False,blank=True,null=True)
    start_triggered = models.BooleanField(default=False,blank=True,null=True)
    variable_json = models.TextField(default=None)

    def save(self):
        print("Calling Send SMS Function")
        super(Campaign, self).save()
        if self.approved == True:
            if self.c_type=='2':
                send = SendSMS.send_sms_fast2sms(self)
            elif self.c_type=='1':
                send_promotional_email(self)


class SendBulkMail(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    target_user = models.IntegerField(null=True, blank=True)
    template_name = models.CharField(max_length=250,null=True, blank=True)
    is_complete = models.BooleanField(default=False,null=True, blank=True)
    json_result = models.TextField(null=True, blank=True)
    location = models.FileField(upload_to="bulk_mail_file", blank=True,null=True)
    approved = models.BooleanField(default=False,blank=False,null=True)

    def save(self):
        print("Calling Send Email Function")
        super(SendBulkMail, self).save()
        if self.approved == True:
            send_bulk_email_comm(self) 
            print("p[[[[[[[[[[")   