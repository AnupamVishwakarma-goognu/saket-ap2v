from django.db import models
from django import forms
from courses.models import Courses
from django.forms import ModelForm
# from batches.models import Batches

class Instructors(models.Model):
    WEEKDAYS_CHOICES=(
                         ('Monday', 'Monday'),
                         ('Tuesday', 'Tuesday'),
                         ('Wednesday', 'Wednesday'),
                         ('Thursday', 'Thursday'),
                         ('Friday', 'Friday'),
                         ('Saturday', 'Saturday'),
                         ('Sunday', 'Sunday')
                     )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=300)
    courses = models.ManyToManyField(Courses, blank=True)
    days_of_week = models.CharField(max_length=600)
    # days_of_week = forms.MultipleChoiceField(choices = WEEKDAYS_CHOICES)
    added_on = models.DateTimeField(auto_now_add=True)
    blue_jeans_user_id = models.CharField(max_length=50,default=0)
    blue_jeans_passcode = models.CharField(max_length=50,default=0)
    user_room_json = models.TextField(null=True, blank= True)
    active = models.BooleanField(default=True,null=True)

    zoom_email = models.CharField(max_length=300,null=True, blank= True,default=None)
    zoom_password = models.CharField(max_length=300,null=True, blank= True,default=None)


    def days_get_function(self):
        return Instructors.WEEKDAYS_CHOICES

    def __str__(self):
        return self.full_name

    @property
    def name(self):
        return self.full_name
        
# class Days_week_multi_selection(ModelForm):
#     days_of_week = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices = WEEKDAYS_CHOICES)
#
#     class Meta:
#         model = Instructors
#         fields = '__all__'
#
#     def clean_days_of_week(self):
#         print(self.cleaned_data)
#         color = self.cleaned_data['days_of_week']
#         # print(color)
#         # if not color:
#         #     raise forms.ValidationError("...")
#
#         # if len(color) > 2:
#         #     raise forms.ValidationError("...")
#
#         days = ','.join(color)
#         return days
