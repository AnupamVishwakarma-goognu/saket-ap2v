# from tkinter.messagebox import NO
from django.db import models
from django.utils import timezone
from courses.models import Courses
from ap2v_courses.models import Courses as ap2vCourse
from instructors.models import Instructors
import re
from users.models import CustomUserModel as User
import uuid


# Create your models here.
class Demo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    batch_name = models.CharField(max_length=300, null=True,blank=True)
    instructors = models.ForeignKey(Instructors, on_delete=models.PROTECT)
    candidates = models.CharField(max_length=300)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    courses = models.ForeignKey(Courses, on_delete=models.PROTECT)
    create_on = models.DateTimeField(default=timezone.now)
    meeting_id = models.CharField(max_length=250,default=0000000, null=True,blank=True)
    moderator_passcode =  models.CharField(max_length=10,default=0000, null=True,blank=True)
    attendee_passcode =  models.CharField(max_length=10,default=0000, null=True,blank=True)
    bitly_link_instructer = models.CharField(max_length=300, null=True,blank=True)
    bitly_link_student_mobile = models.CharField(max_length=300, null=True,blank=True)
    bitly_link_student_desktop = models.CharField(max_length=300, null=True,blank=True)
    descard = models.BooleanField(default=False, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, null=True)

    zoom_meeting_id = models.CharField(max_length=250,default=None,null=True,blank=True)
    zoom_meeting_password = models.CharField(max_length=250,default=None,null=True,blank=True)
    zoom_bitly_link_instructer = models.TextField(default=None,null=True,blank=True)
    zoom_bitly_link_student_mobile = models.TextField(default=None,null=True,blank=True)
    zoom_response_logs = models.TextField(default=None,null=True,blank=True)

    def __str__(self):
        return "{}-{}({})".format(self.id,self.instructors.name,self.courses.name)


class DemoSMSTemplate(models.Model):
    create_on = models.DateTimeField(default=timezone.now)
    template_name = models.CharField(max_length=100, blank=True,null=True)
    template_text = models.TextField(help_text="Please Use: {name},{course},{datetime},{link}")
    variable_count = models.IntegerField(blank=True,null=True, help_text="Leave blank this field")

    def __str__(self):
        return self.template_name

    def save(self):
        count = len(re.findall(r'{(.*?)}', self.template_text))

        self.variable_count = count
        super(DemoSMSTemplate, self).save()
    
class DemoSaveVideo(models.Model):
    course_name=models.ForeignKey(ap2vCourse, on_delete=models.PROTECT)
    file_name=models.CharField(max_length=100, blank=True,null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    video_uload = models.FileField(upload_to='demovideo', default=None)

    # def __str__(self):
    #     return self.course_name