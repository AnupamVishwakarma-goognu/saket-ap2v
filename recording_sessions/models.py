from itertools import chain
from unicodedata import name
from django.db import models
from django.forms import CharField
from ap2v_courses.models import Courses
from users.models import CustomUserModel as User
from batches.models import CompleteRecording,Batches


# Create your models here.

class Recorded_Courses_name(models.Model):
    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING, null=True)
    status=models.BooleanField(default=False, null=True, blank=True)
    number=models.IntegerField(default=1)
    
    def __str__(self):
        return self.course.name


class Recorded_Uploading_S3_Logs(models.Model):
    course_name=models.ForeignKey(Recorded_Courses_name,on_delete=models.DO_NOTHING, null=True)
    name=models.CharField(max_length=250, blank= False)
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False, null=True, blank=True)
    # upload = models.BooleanField(default=False, null=True, blank=True)
   

    def __str__(self):
        return self.course_name.course.name

class Purchased_classroom_recording_course(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    course_name=models.ForeignKey(Recorded_Courses_name,on_delete=models.DO_NOTHING, null=True)

class temp_recored_detail(models.Model):
    user=models.CharField(max_length=250, blank= False)
    course=models.CharField(max_length=250, blank= False)
    price=models.IntegerField()
    email=models.EmailField(max_length=250, blank= False)
    date=models.DateTimeField(auto_now_add=True)

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

class Order(models.Model):

    name = models.ForeignKey( User, on_delete=models.DO_NOTHING, null=True)
    amount = models.FloatField( null=False, blank=False)
    courses=models.ManyToManyField(Courses)
    status = models.CharField(
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField( max_length=40, null=False, blank=False)
    payment_id = models.CharField( max_length=36, null=False, blank=False )
    signature_id = models.CharField( max_length=128, null=False, blank=False)

    # def __str__(self):
    #     return f"{self.id}-{self.name}-{self.status}"
from ap2v_e_store.models import CourseStoreCart

class temp_order_detail(models.Model):
   user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
   course=models.ManyToManyField(CourseStoreCart)
   order_id = models.CharField( max_length=36, null=False, blank=False )
   date=models.DateTimeField(auto_now_add=True)
#    cart=models.ManyToManyField(CourseStoreCart)


class OnlineBuyedCourse(models.Model):
    COURSE_TYPE=(
        ('1', 'Recorded'),
        ('2', 'Online'),
    )
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING, null=True)
    order=models.ForeignKey(Order,on_delete=models.DO_NOTHING, null=True)
    date=models.DateTimeField(auto_now_add=True)
    course_type = models.CharField(max_length=2,choices=COURSE_TYPE,default='1')
    batch_id=models.ForeignKey(Batches,on_delete=models.DO_NOTHING, null=True)






