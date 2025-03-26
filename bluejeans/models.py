from django.db import models
from django.utils import timezone

# Create your models here.
class AccessToken(models.Model):
    date = models.DateField(default=timezone.now)
    access_token = models.CharField(max_length=250)
    user = models.CharField(max_length=250)
    enterprise = models.CharField(max_length=250)