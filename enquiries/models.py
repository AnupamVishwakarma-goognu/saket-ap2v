from django.db import models
from courses.models import Courses
from datetime import datetime, timedelta, time
from django.utils import timezone
from anquira_v2.anquira_handlers import (
    TrainingModeChoices, ReferenceModeChoices, EnquiryLevelChoices,
    AssignedByChoices
)
from anquira_v2.utils import tat_algorithm

class StudentResponse(models.Model):
    response = models.CharField(max_length=120)
    priority=models.PositiveSmallIntegerField(default=1,help_text="1 is higher than 2")
        
    def __str__(self):
        return "{0}".format(self.response)


class Enquiries(models.Model):
    WEEKDAYS_CHOICES=(
                     (1, 'Monday'),
                     (2, 'Tuesday'),
                     (3, 'Wednesday'),
                     (4, 'Thursday'),
                     (5, 'Friday'),
                     (6, 'Saturday'),
                     (7, 'Sunday'),

                     )
    SELECT_REFERENCE = (
            ('website', 'website'),
            ('google', 'google'),
            ('walk-in', 'walk-in'),
            ('self', 'self')
        )

    BRANCH_LOCATION = (
            ('gurgaon', 'gurgaon'),
            ('noida', 'noida')
        )
    attended = models.BooleanField(default=False)
    reference = models.CharField(max_length=250, choices=ReferenceModeChoices.choice, null= True,default='ap2v.com')
    email = models.EmailField()
    alternative_email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=50,default="+91")
    mobile = models.CharField(max_length=300)
    alternative_mobile = models.CharField(max_length=300, null=True, blank=True)
    company_name = models.CharField(max_length=300,default="N/A",null=True,)
    designation = models.CharField(max_length=300,default="N/A",null=True,)
    courses = models.ManyToManyField(Courses, blank=True)
    batch_days = models.CharField(max_length=255,default="N/A",null=True,)
    enquiry_level = models.PositiveSmallIntegerField(default=1, choices=EnquiryLevelChoices.choice)
    tmp_discard = models.BooleanField(default=False, null=True, blank=True)
    training_mode = models.PositiveSmallIntegerField(default=1, choices=TrainingModeChoices.choice)
    batch_time = models.CharField(max_length=255, default=True)
    branch_location = models.CharField(max_length=300, choices = BRANCH_LOCATION, null= True)
    # assigned_by = models.PositiveIntegerField(default=9, null=True, blank=True, choices=AssignedByChoices.choice)
    assigned_by = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
    interested_batch = models.BooleanField(default=False)
    next_followup = models.DateTimeField(default=None,null=True, blank=True)
    source_ip = models.CharField(max_length=300, null=True, blank=True, default="N/A")
    comments = models.TextField(null=True, blank=True, default="N/A")
    # tat = models.CharField(max_length=10, null=True, blank=True, default=None)
    added_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True, default="N/A")
    assigned_on = models.DateTimeField(default=timezone.now)
    update_on = models.DateTimeField(default=None,null=True, blank=True,)
    junk = models.BooleanField(null=True, blank=True, default=False)
    calling_datetime = models.CharField(null=True, blank=True, default=None,max_length=255)
    def __str__(self):
        # return "id: %d:, fullname: %s, email: %s, source_ip: %s, reference: %s" % (self.id, self.full_name, self.email, self.source_ip, self.reference)
        return "id: %d:, fullname: %s" % (self.id, self.full_name)

    def save(self):
        self.update_on = timezone.now()
        self.full_name = self.full_name.title()
        super(Enquiries, self).save()

    @property
    def mode_display(self):
        return self.get_training_mode_display()

    @property
    def courses(self):
        courses = EnquiryCourses.objects.filter(enquiry_id=self)
        return ','.join(courses.values_list('courses__name',flat=True))

    @property
    def nostatus_courses(self):
        courses = EnquiryCourses.objects.filter(enquiry_id=self, status=EnquiryCourses.NONE)
        return ','.join(courses.values_list('courses__name',flat=True))

    class Meta:
        ordering = ['-id']

    def discard_action(self,new_discard_status=True,reason=''):
        '''
        Upon discarding an enquiry this method will update all pending(non enrolled)
        courses into discarded status, and upon undiscard will update the discarded
        courses into None status i.e. pending
        this is central method to update any status of enquiry
        '''
        courses=EnquiryCourses.objects.filter(enquiry_id=self)
        is_none,is_discarded=EnquiryCourses.NONE,EnquiryCourses.DISCARDED
        if new_discard_status:
            comment=''
            if reason:
                comment="{}:{}".format(datetime.now().strftime( '%Y-%m-%d'),reason)
            courses.filter(status=is_none).update(status=is_discarded,comment=comment)
        else:
            courses.filter(status=is_discarded).update(status=is_none)
        
        return 
        self.discard=new_discard_status
        self.save()

        EnquiryCourses.objects.filter(enquiry_id=self).update(discard=new_discard_status)
        #only discard the old followups, do not undiscard old followups
        if new_discard_status:
            Followups.objects.filter(followupid=self).update(discard=new_discard_status)

    @property
    def last_comment(self):
        today = datetime.now().date()
        today_start = datetime.combine(today, time())
        fu=Followups.objects.filter(followupid=self, next_followup__gte=today_start).order_by('next_followup').first()
        return fu.comments if fu else '-'
    
    @property
    def latest_comment(self):
        comments = '-'
        followups_obj = Followups.objects.filter(followupid = self.id).last()
        if followups_obj:
            comments = followups_obj.comments
            print("---------------------------")
            print(comments)
        return comments

    @property
    def discard(self):
        courses=EnquiryCourses.objects.filter(enquiry_id=self)
        is_none,is_discarded=EnquiryCourses.NONE,EnquiryCourses.DISCARDED
        if courses.filter(status=is_none).count():
            return False

        return True
    
    def tat_display(self):
        print(self.id)
        print("---------------------")
        fu = Followups.objects.filter(followupid=self).first()
        if fu:
            print(fu.added_on)
            print(self.added_on)
            tat = tat_algorithm(self.added_on,fu.added_on)
            print(tat)
            return tat
        return "N/A"

        
class EnquiryCourses(models.Model):
    class Meta:
        unique_together = (('enquiry_id', 'courses'),)

    NONE=0
    ENROLLED=1
    DISCARDED=2
    choices=(
        (NONE,'None'),
        (ENROLLED,'Enrolled'),
        (DISCARDED,'Discarded')
    )

    enquiry_id = models.ForeignKey(Enquiries, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    status=models.PositiveSmallIntegerField(choices=choices,default=NONE)
    #following two fields need to be removed after data correction
    comment=models.CharField(max_length=255,null=True,blank=True)
    tmp_discard = models.BooleanField(default=False,null=True,blank=True)
    enroll = models.BooleanField(default=False, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} - {} ({})".format(self.id, self.enquiry_id, self.courses)

    # class Meta:
    #     unique_together = ['enquiry_id','courses']

class Followups(models.Model):
    TYPES_OF_FOLLOWUPS = (
        ('email', 'email'),
        ('call', 'call'),
        ('walk-in', 'walk-in')
    )

    TYPES_OF_FOLLOWUPS_MODE = (
        ('visit', 'visit'),
        ('call', 'call'),
        ('email', 'email')
    )


    followupid = models.ForeignKey(Enquiries, on_delete=models.SET_NULL,null=True)
    # enquiry_courses = models.ForeignKey(EnquiryCourses, on_delete=models.PROTECT)
    followup_mode = models.CharField(max_length=300, choices=TYPES_OF_FOLLOWUPS_MODE)
    response = models.CharField(max_length=300, choices=TYPES_OF_FOLLOWUPS)
    next_followup = models.DateTimeField(null = True)
    comments = models.TextField()
    status = models.BooleanField(default=False, null=True, blank=True)
    is_complete = models.BooleanField(default=False, null=True, blank=True)
    discard = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    assigned_user = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField( auto_now_add=True)
    student_response = models.ForeignKey(StudentResponse, on_delete=models.SET_NULL, null=True)
    
    @property
    def sys_id(self):
        return "FOL-{}".format(str(self.id + 1000).zfill(6))

    @property
    def last_comment(self):
        #fl=Followups.objects.filter(followupid=self.followupid).order_by('added_on').last()
        fl=Followups.objects.get(followupid=self.followupid)
        if fl:
            return fl.comments
        return '-'

class InformationSharingTemplate(models.Model):
    EMAIL=1
    SMS=2
    SEND_TYPE_CHOICES=(
        (EMAIL,'Email'),
        (SMS,'SMS'),
    )

    COURSE=1
    ACCOUNT_DETAILS=2
    TYPE_CHOICES=(
        (COURSE,'Course'),
        (ACCOUNT_DETAILS,'Account Detail'),
    )

    subject = models.CharField(max_length=255,blank=True,help_text="Keep this blank for sms")
    body = models.TextField(help_text="Variables available; username,course_name,course_url,course_duration,course_price; use like eg. {username}")
    send_type=models.PositiveIntegerField(choices=SEND_TYPE_CHOICES,default=EMAIL)
    type=models.PositiveIntegerField(choices=TYPE_CHOICES,default=COURSE)

    def __str__(self):
        return "{0} ({1})".format(self.get_send_type_display(), self.get_type_display())

    def __unicode__(self):
        return "{0} ({1})".format(self.get_send_type_display(), self.get_type_display())

    class Meta:
        ordering = ['-id']


class EduzillaComments(models.Model):
    uid=models.IntegerField()
    stud_details=models.TextField()
    comments=models.TextField()


class ReassignedEnquiryLogs(models.Model):
    enquiry = models.ForeignKey(Enquiries, on_delete=models.SET_NULL, null=True)
    from_counselor = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True, related_name = "form_counselor")
    to_counselor = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True, related_name = "to_counselor")
    assigned_on = models.DateTimeField(default=timezone.now)