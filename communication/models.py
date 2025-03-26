from django.db import models

# Create your models here.

class CounselorContactNumber(models.Model):
    # user = models.ForeignKey(User, related_name='user',on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=20, null=False,blank=False)
    name = models.CharField(max_length=50, null=False,blank=False)
    used_number = models.BooleanField(default=False,null=False,blank=False)