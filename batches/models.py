from pyexpat import model
from urllib import response
from django.db import models
from django.utils import timezone
from courses.models import Courses
from instructors.models import Instructors
from enrolls.models import Enrollments
import uuid
from enrolls.models import Enrollments
from demo.models import Demo

class Batches(models.Model):

    WEEKDAYS_CHOICES=(
                         (1, 'Monday'),
                         (2, 'Tuesday'),
                         (3, 'Wednesday'),
                         (4, 'Thursday'),
                         (5, 'Friday'),
                         (6, 'Saturday'),
                         (7, 'Sunday'),

                     )
    BATCH_STATUS=(
        ('1', 'Mark as complete'),
        ('2', 'Mark as merge'),
        ('3', 'Mark as discontinue'),
        ('4', 'Mark as Running'),
        ('5', 'Mark as complete by instructor'),
    )
    BATCH_TYPE=(
        ('1', 'Regular'),
        ('2', 'Backup'),
    )
    LANGUAGE_TYPE=(
        ('0', 'None'),
        ('1', 'Hindi'),
        ('2', 'English'),
    )
    batch_name = models.CharField(max_length=300, null=True)
    days_of_week = models.CharField(max_length=300)
    duration = models.PositiveIntegerField( null = True)
    session_duration = models.PositiveIntegerField(default=1)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True,blank=True, default=None)
    instructors = models.ForeignKey(Instructors, on_delete=models.PROTECT)
    instructor_blue_jeans_user_id = models.CharField(max_length=250,null=True, blank=True,default=None)
    create_on = models.DateTimeField(default=timezone.now)
    # courses = models.ForeignKey(Courses, on_delete=models.PROTECT)
    candidates = models.CharField(max_length=300)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True,blank=True, default=None)
    complete = models.BooleanField(blank=True, null=True, default=False)
    meeting_id = models.CharField(max_length=250,default=0000000)
    moderator_passcode =  models.CharField(max_length=10,default=0000)
    attendee_passcode =  models.CharField(max_length=10,default=0000)
    chat_room_id = models.CharField(max_length=250,default=None,null=True,blank=True)
    # course_content = models.FileField(upload_to = 'files/', null = True, blank = True)
    bitly_link_instructer = models.CharField(max_length=300, null=True,blank=True)
    bitly_link_student_mobile = models.CharField(max_length=300, null=True,blank=True)
    bitly_link_student_desktop = models.CharField(max_length=300, null=True,blank=True)
    enroll_student = models.ManyToManyField("enrolls.Enrollments", default=None, blank=True)
    courses = models.ManyToManyField(Courses, default=None, blank=True)
    certificate_issued = models.BooleanField(blank=True, null=True, default=False)
    student_attendance = models.TextField(null=True, blank=True,default=None)
    last_join_datetime = models.DateTimeField(null=True,blank=True, default=None)
    is_alert_send = models.BooleanField(blank=True, null=True, default=False)
    batch_status = models.CharField(max_length=2,choices=BATCH_STATUS,default='4')
    reminder_log = models.TextField(null=True, blank=True,default=None)
    batch_type = models.CharField(max_length=2,choices=BATCH_TYPE,default='1')
    language_type = models.CharField(max_length=2,choices=LANGUAGE_TYPE,default='0')

    zoom_meeting_id = models.CharField(max_length=250,default=None,null=True,blank=True)
    zoom_meeting_password = models.CharField(max_length=250,default=None,null=True,blank=True)
    zoom_bitly_link_instructer = models.TextField(default=None,null=True,blank=True)
    zoom_bitly_link_student_mobile = models.TextField(default=None,null=True,blank=True)
    zoom_response_logs = models.TextField(default=None,null=True,blank=True)


    def __str__(self):
        course_name =  self.courses.all()
        cour = [i.name for i in course_name]
        # print(cour)
        # print(type(cour))
        rtn_str = "{}-{}({})".format(self.id,self.instructors.full_name," & ".join(cour))
        return rtn_str

    def calculate_end_time(self, batch_start_date_time, session_duration, course_duration, batch_week_days):
        from datetime import datetime, timedelta
        return datetime.now()
        total_sessions = int(course_duration) / int(session_duration)
        # batch_start_date_time_obj = datetime.strptime(batch_start_date_time, '%m/%d/%Y %I:%M %p')
        days_ago = 0
        while total_sessions > 0:
            batch_end_date_time = self.start_date_time + timedelta(days=days_ago, hours=session_duration)
            if batch_end_date_time.weekday() in batch_week_days:
                total_sessions -= 1
            days_ago += 1
        return batch_end_date_time

    @property
    def get_end_time(self):
        from datetime import datetime, timedelta

        week_days = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

        a = float(str(timedelta(minutes=self.session_duration)).replace(":", ".")[:-3])

        end_time = self.calculate_end_time(
            self.start_date_time,
            a if a <= 0 else 1,
            self.courses.duration,
            [week_days.get(i) for i in self.days_of_week.split(',')]
            )
        date_var, time_var = end_time.date(), end_time.time()
        return {
            "view": "{0}T{1}".format(date_var, time_var),
            "list": "{0} {1}".format(date_var, time_var)
        }

    @property
    def get_update_created_dates(self):
        if self.updated_on:
            return {
                'added_on': "{0}T{1}".format(
                                self.create_on.date(),
                                self.create_on.time()
                            ).split('.')[0],
                'updated_on': "{0}T{1}".format(
                                self.updated_on.date(),
                                self.updated_on.time()
                            ).split('.')[0]
                }
        else:
            return {
                'added_on': "{0}T{1}".format(
                                self.create_on.date(),
                                self.create_on.time()
                            ).split('.')[0],
                }

class StudentCertificateIssued(models.Model):
    name = models.CharField(max_length=300, null=True)
    course = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(null=True,blank=True, default=None)
    code = models.CharField(max_length=300, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batches, on_delete=models.SET_NULL, null=True)
    enroll = models.ForeignKey(Enrollments,on_delete=models.SET_NULL, null=True)

class BestRecording(models.Model):
    BATCH_TYPE = (
        ('1', 'Batch'),
        ('2', 'Demo-Batch'),
        )
    create_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=2,choices=BATCH_TYPE,default=None)
    link = models.TextField(null=True,blank=True)
    batch_demo_id = models.CharField(max_length=300, null=True)
    batch_name = models.CharField(max_length=300, null=True)

class BatchSessionOff(models.Model):
    added_on = models.DateField(auto_now_add=True)
    batch = models.ForeignKey(Batches,on_delete=models.SET_NULL, null=True)
    off_date = models.DateField(null=False,blank=False)

class UnsubscribeBatchReminderEmail(models.Model):
    added_on = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=250,null=False,blank= False)

class PublicHoliday(models.Model):
    added_on = models.DateField(auto_now_add=True)
    occasion = models.TextField(null=True,blank=True)
    off_date = models.DateField(null=False,blank=False)

class ZoomMeetingIdUserBatch(models.Model):
    MEETING_STATUS = (
        ('1', 'Active'),
        ('2', 'Ended'),
        )
    MEETING_TYPE = (
        ('1', 'Batch'),
        ('2', 'Demo'),
        )

    date = models.DateTimeField(auto_now_add=True)
    meeting_type = models.CharField(max_length=2,choices=MEETING_TYPE,default=None)
    batch = models.ForeignKey(Batches,on_delete=models.SET_NULL, null=True,blank=True)
    demo = models.ForeignKey(Demo,on_delete=models.SET_NULL, null=True,blank=True)
    meeting_id = models.CharField(max_length=250,null=True, blank=True)
    meeting_status = models.CharField(max_length=2,choices=MEETING_STATUS,default=None)
    zoom_meeting_password = models.CharField(max_length=250,default=None,null=True,blank=True)
    zoom_bitly_link_instructer = models.TextField(default=None,null=True,blank=True)
    zoom_bitly_link_student_mobile = models.TextField(default=None,null=True,blank=True)
    zoom_response_logs = models.TextField(default=None,null=True,blank=True)
    meeting_start_at = models.DateTimeField(null=True,blank=True, default=None)
    meeting_end_at = models.DateTimeField(null=True,blank=True, default=None)

# class ZoomMeetingIdUserDemo(models.Model):
#     MEETING_STATUS = (
#         ('1', 'Active'),
#         ('2', 'Ended'),
#         )

#     date = models.DateTimeField(auto_now_add=True)
#     demo = models.ForeignKey(Demo,on_delete=models.SET_NULL, null=True)
#     meeting_id = models.CharField(max_length=250,null=True, blank=True)
#     meeting_status = models.CharField(max_length=2,choices=MEETING_STATUS,default=None)
#     zoom_meeting_password = models.CharField(max_length=250,default=None,null=True,blank=True)
#     zoom_bitly_link_instructer = models.TextField(default=None,null=True,blank=True)
#     zoom_bitly_link_student_mobile = models.TextField(default=None,null=True,blank=True)
#     zoom_response_logs = models.TextField(default=None,null=True,blank=True)
#     meeting_start_at = models.DateTimeField(null=True,blank=True, default=None)
#     meeting_end_at = models.DateTimeField(null=True,blank=True, default=None)

class ZoomWeebHookResponce(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    response = models.TextField(default=None,null=True,blank=True)
    response_type_log = models.TextField(default=None,null=True,blank=True)

class ZoomLicenseDetails(models.Model):
    total_license = models.IntegerField(default=0,null=False,blank=False)
    use_license = models.IntegerField(default=0,null=False,blank=False)


class CompleteRecording(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.SET_NULL, null=True,blank=True)
    batch = models.ForeignKey(Batches,on_delete=models.SET_NULL, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
