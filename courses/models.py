from multiprocessing.dummy import active_children
# from tkinter import ACTIVE
from django.db import models
from django.utils import timezone
from anquira_v2 import choices

class Courses(models.Model):
    name = models.CharField(max_length=300)
    duration = models.IntegerField()
    url = models.URLField()
    price = models.IntegerField()
    course_content = models.FileField(null=True, blank=True, help_text="Course content")
    is_exam = models.BooleanField(default=False, null=True, blank=True)
    # typee = models.SmallIntegerField(choices = choices.CourseType.CHOICES, default=0) # use typee because type is reserve  keyword
    is_expired = models.BooleanField(default=False, null=True, blank=True)
    is_gst = models.BooleanField(default=False, null=True, blank=True) # is GST Applicable on this Course price
    original_price = models.IntegerField(null=False, blank=False,default=0,help_text="This is course original price, WITHOUT DISCOUNT.")
    def __str__(self):
        return self.name


class Exams(models.Model):
    exam_name = models.CharField(max_length=300)
    courses = models.ForeignKey(Courses, on_delete=models.PROTECT)

    def __str__(self):
        return self.exam_name

class Books(models.Model):
    course_book = models.ForeignKey(Courses,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=300)
    cost = models.CharField(max_length=300)
    course = models.CharField(max_length=300)
    added_on = models.DateField(default=timezone.now)
    stock = models.IntegerField(default=0, null=True, blank=True)
    book_content = models.FileField(null=True, blank=True, help_text="book content")
