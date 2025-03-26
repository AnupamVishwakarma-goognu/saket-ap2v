from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from anquira_v2 import choices

class CustomUserModel(AbstractUser):
    LOCATION = (
        ("all", "all"),
        ('gurgaon', 'gurgaon'),
        ('noida', 'noida')
    )

    USER_TYPE = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('counselor', 'Counselor'),
        ('partner', 'Partner'),
        ('no_role','No Role')
    )
    exist_employee = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20,blank=True)
    location = models.CharField(max_length=15,choices=LOCATION,default="ALL")
    user_type = models.CharField(max_length=25,choices=USER_TYPE,default='student')
    is_verified = models.BooleanField(default = True, null=True)
    # @property
    # def name(self):
    #     return self.get_full_name()
    def __str__(self):
        return self.username

class CounselorPreferences(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True,limit_choices_to={'user_type':'counselor'})
    last_assigned = models.BooleanField(default=False)

# class StudentPreferences(models.Model):
#     user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True)

# class InstructorPreferences(models.Model):
#     user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True)

class PartnerPreferences(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True,limit_choices_to={'user_type':'partner'})

class UserRegistrationVerification(models.Model):
    name = models.CharField(max_length=50,blank=True)
    password = models.CharField(max_length=50,blank=True)
    email = models.CharField(max_length=50,blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=50,blank=False,unique = True)
    uuid = models.CharField(max_length=255,blank=False,unique = True)

class UserPasswordResetVerification(models.Model):
    email = models.CharField(max_length=50,blank=True)
    token = models.CharField(max_length=50,blank=False,unique = True)
    uuid = models.CharField(max_length=255,blank=False,unique = True)
    date = models.DateTimeField(auto_now=True,blank=True)


def from_500():
    largest = CertificateId.objects.all().order_by('cert_id').last()
    if not largest:
        return 4184
    return largest.cert_id + 1


class CertificateId(models.Model):
    cert_id = models.IntegerField(primary_key=True,default=from_500)
    user = models.OneToOneField(CustomUserModel,on_delete=models.SET_NULL, null=True)