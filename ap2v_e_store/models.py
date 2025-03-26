from django.db import models
from users.models import CustomUserModel as User
from recording_sessions.models import Recorded_Courses_name
from ap2v_courses.models import Courses
from batches.models import CompleteRecording,Batches


# Create your models here.
class CourseStoreCart(models.Model):
    COURSE_TYPE=(
        ('1', 'Recorded'),
        ('2', 'Online'),
    )
    date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    course = models.ForeignKey(Courses,on_delete=models.DO_NOTHING, null=True)
    course_type = models.CharField(max_length=2,choices=COURSE_TYPE,default='1')
    batch_course = models.ForeignKey(Batches,on_delete=models.DO_NOTHING, null=True)
    available_lang = models.CharField(max_length=10,null=True )

