from django.db import models
from users.models import CustomUserModel as User
from batches.models import Batches
from ap2v_courses.models import Courses
from home.models import Category
from django.utils import timezone
from datetime import datetime




# Create your models here.

class BatchStudentFeedback(models.Model):
    datetime = models.DateField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    batch = models.ForeignKey(Batches, on_delete=models.SET_NULL,null=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True,default=None)


class ClassRoomCourseOffer(models.Model):
    course = models.ForeignKey("ap2v_courses.Courses", on_delete=models.SET_NULL,null=True,related_name="offer_course")
    discount=models.IntegerField(null=True, blank=True, default=0, help_text="<h3> Discount in %, Example 10%, 20% <br><span style='background-color:yellow;'>NOTE: Don't use % symbol.</span></h3>")
    discount_valid_till = models.DateField(null=True,blank=True, help_text="<h4>NOTE: Above discount valid till date.</h4>")
    discount_after_date = models.IntegerField(null=True, blank=True, default=0, help_text="<h4>if <span style='color:black'>Discount valid till:</span> date pass then <span style='color:black'>Discount after date<span> discount will be applicable.</h4>")
    relevant_course = models.ManyToManyField("ap2v_courses.Courses")

class StudyMaterial(models.Model):
    batch_id = models.ForeignKey(Batches, on_delete=models.CASCADE)
    file = models.FileField(upload_to='study_materials/')

    def _str_(self):
        return f"Study Material for Batch {self.batch_id}"    