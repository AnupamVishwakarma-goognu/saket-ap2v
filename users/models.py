from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager,AbstractBaseUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from anquira_v2 import choices

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser):
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
    username = models.CharField(max_length=50,unique=True,blank=True,null=True)
    email = models.CharField(max_length=100,unique=True,blank=True)
    exist_employee = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    location = models.CharField(max_length=15,choices=LOCATION,default="ALL")
    user_type = models.CharField(max_length=25,choices=USER_TYPE,default='student')
    is_verified = models.BooleanField(default = True, null=True)
    objects=MyUserManager()
    date_joined = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True    

class CounselorPreferences(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True,limit_choices_to={'user_type':'counselor'})
    last_assigned = models.BooleanField(default=False)



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