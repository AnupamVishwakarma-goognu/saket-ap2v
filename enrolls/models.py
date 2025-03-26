from django.db import models
from enquiries.models import Enquiries, EnquiryCourses
# from batches.models import Batches
from courses.models import Courses,Books
from users.models import CustomUserModel, PartnerPreferences
from django.utils import timezone
from anquira_v2 import choices
# class Fees(models.Model):
#     amount = models.IntegerField()
#     date = models.DateField()
#     FEES_PAID_OR_NOT = (
#         (1, 'paid'),
#         (0, 'unpaid')
#     )
#     status = models.BooleanField(default=False, choices=FEES_PAID_OR_NOT)

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100, help_text="Payment Method")
    gst_applicable=models.BooleanField(default=False)
    def __str__(self):
        return self.payment_method

class Enrollments(models.Model):
    ENROLL_TYPE =(
        ('1','Fresh Enrollment'),
        ('2','Rivision Enrollment'),
    )
    COURSE_TYPE=(
        ('1', 'Recorded'),
        ('2', 'Live'),
    )
    
    enquiry_course_id = models.ForeignKey(EnquiryCourses, on_delete=models.PROTECT)
    # batch = models.ForeignKey(Batches, on_delete=models.PROTECT, null=True, blank=True)
    # email = models.EmailField(null = True)
    #assigned_batches = models.ForeignKey(Batches, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    discussed_fee = models.IntegerField()
    discussed_fee_gst = models.IntegerField(null=True,default=0)
    # registration_amount = models.IntegerField(help_text="Enter registration amount")
    registered_on = models.DateTimeField(auto_now=True)
    #registered_by = models.CharField(max_length = 255, null = True) # ForeignKey users
    registered_by = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    enroll_courses = models.CharField(max_length=255,blank=True,null=True,default=None)
    batch = models.CharField(max_length=255,blank=True,null=True, default=None)
    refund = models.BooleanField(null=True, blank=True, default=False)
    refund_amount = models.CharField(max_length=6,null=True, blank=True, default=None)
    dropped = models.BooleanField(null=True, blank=True, default=False)
    dropped_on = models.DateField(null=True, blank=True, default=None)
    certificate_issued = models.BooleanField(null=True, blank=True, default=False)
    certificate_uuid = models.CharField(max_length=255,null=True, blank=True, default=None)
    enroll_type = models.CharField(max_length=10,null=True, blank=True, default="1",choices=ENROLL_TYPE)
    parent_enrollment_id = models.CharField(max_length=10,null=True, blank=True, default=None)
    exam_share = models.FloatField(blank=True,null=True,default=0)
    book_share = models.FloatField(blank=True,null=True,default=0)
    vandor_share = models.FloatField(blank=True,null=True,default=0)
    other_share = models.FloatField(blank=True,null=True,default=0)
    ap2v_share = models.FloatField(blank=True,null=True,default=0)
    ap2v_share_recived = models.FloatField(blank=True,null=True,default=0)
    current_recived_amount = models.FloatField(blank=True,null=True,default=0)
    course_type = models.CharField(max_length=10,choices=COURSE_TYPE,default='2')
    


    def __str__(self):
        return self.enquiry_course_id.enquiry_id.full_name

class Installments(models.Model):
    enrollmentid = models.ForeignKey(Enrollments, on_delete=models.PROTECT, null=True)
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.PROTECT)
    installment_no = models.IntegerField(default=0)
    installment = models.IntegerField()
    due_date = models.DateField()
    comment = models.CharField(max_length=255,blank=True,null=True)
    paid_unpaid = models.BooleanField(default = False)
    added_on = models.DateTimeField(
        auto_now_add = True
    )
    updated_on = models.DateTimeField(
        auto_now = True
    )
    attachment = models.FileField(upload_to="installment/attachment",default=None,blank=True, null=True)
    fee_type= models.IntegerField(choices=choices.FeeType.CHOICES,default=1)
    paid_on = models.DateField(null=True, blank=True)

    @property
    def get_update_created_dates(self):
        return {
            'added_on': "{0}T{1}".format(
                            self.added_on.date(),
                            self.added_on.time()
                        ).split('.')[0],
            'updated_on': "{0}T{1}".format(
                            self.updated_on.date(),
                            self.updated_on.time()
                        ).split('.')[0],
            'due_date': self.due_date.strftime('%m/%d/%Y')
            }

    # installment_no = models.IntegerField(null=True, default=0)
    #
    # def save(self, *args, **kwargs):
    #     self.installment_no += Installments.objects.filter(enrollment=self.enrollmentid).count()
    #     super(Installments, self).save(*args, **kwargs)

    #
    # @property
    # def sys_id(self):
    #     return "FOL-{}".format(str(self.id + 1000).zfill(6))


# class EnrollCourse(models.Model):
#     enrollments_id = models.ForeignKey(Enrollments, on_delete=models.CASCADE)
#     courses_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
#     added_on = models.DateTimeField(auto_now_add=True)


class PartnerPayment(models.Model):
    partner = models.ForeignKey(PartnerPreferences, on_delete=models.SET_NULL,null=True,blank=True)
    enrollment = models.ForeignKey(Enrollments, on_delete=models.SET_NULL,null=True,blank=True)
    amount = models.IntegerField(default=0, null=True, blank=True)
    is_paid = models.BooleanField(default=False,null=True, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    added_on = models.DateField(null=True, blank=True ,auto_now_add=True)
    added_by = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, blank=True,null=True,related_name="added_by_user")
    updated_by = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL,blank=True, null=True,related_name="updated_by_user")

class SharedBooks(models.Model):
    enrollments = models.ForeignKey(Enrollments, on_delete=models.PROTECT, null=True)
    book = models.ForeignKey(Books, on_delete=models.PROTECT, null=True)
    is_shared = models.BooleanField(default=False,null=True, blank=True)
    shared_on = models.DateField(null=True, blank=True, default=timezone.now)

class Screenshot(models.Model):
    attachment = models.FileField(upload_to="installment/attachment",default=None,blank=True, null=True)