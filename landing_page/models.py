# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ap2v_courses.models import Courses

# Create your models here.

class LandingPageInstructors(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    company = models.CharField(max_length=250, null=True, blank=True)
    company_logo = models.ImageField(upload_to='images/', null=True,default = 'images/instructor_image/certificate.jpg', blank=True)
    designation = models.CharField(max_length=250, null=True, blank=True)
    about_instructor = models.CharField(max_length=250, null=True, blank=True,help_text="NOTE: <h2>About instructor: text content limit is 25-35 word<h/2>")

    def __str__(self):
        return self.name

class Landing_Page(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    slug = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    overview_point = models.TextField(null=True, blank=True, help_text="Every point must be comma separated. Ex: 24*7 support with dedicated mentoring sessions,DevOps methodologies,")
    skill_covered = models.CharField(max_length=250, null=True, blank=True, help_text="Every point must be comma separated")
    # syllabus_url = models.CharField(max_length=100, null=True, blank=True)
    # syllabus = models.FileField(upload_to='syllabus/', null=True,default = '', blank=True)
    advisor_number = models.CharField(max_length=250, null=True, blank=True)
    # anquira_course = models.IntegerField(null=True, blank=True)
    anquira_reference = models.CharField(max_length=250, null=True, blank=True, help_text="YoCreativ-AdWords")
    student_enrolled = models.CharField(max_length=250, null=True, blank=True)
    duration = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    hiring_partners = models.CharField(max_length=250, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    emi = models.IntegerField(null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)
    instructor = models.ManyToManyField(LandingPageInstructors)

    
    def __str__(self):
	    return self.title


class SoftwareTools(models.Model):
    belong_landing_page = models.ForeignKey(Landing_Page, on_delete=models.CASCADE)
    alt_text = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True,default = 'images/course-detail/certificate.jpg', blank=True)


class ExamCertification(models.Model):
    belong_landing_page = models.ForeignKey(Landing_Page, on_delete=models.CASCADE)
    exam_certification_title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    exam_certification_image = models.ImageField(upload_to='images/', null=True,default = 'images/course-detail/certificate.jpg', blank=True)


class Projects(models.Model):
    belong_landing_page = models.ForeignKey(Landing_Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Testimonial(models.Model):
    belong_landing_page = models.ForeignKey(Landing_Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True,default = 'images/course-detail/certificate.jpg', blank=True)

