# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from ap2v_courses.models import Courses
# Create your models here.

class Text(models.Model):
    course=models.ForeignKey(Courses, on_delete=models.DO_NOTHING,null=True, blank=True)
    name = models.CharField(max_length = 60,null = True, blank = True)
    designation = models.CharField(max_length = 60,null = True, blank = True)
    company = models.CharField(max_length = 60,null = True, blank = True)
    rating = models.FloatField(max_length = 5)
    content = models.TextField(max_length=1024,null = True, blank = True)
    date = models.DateField( blank=True)
    image = models.ImageField(upload_to = 'images/testimonials/' , default= 'static/images/courses/no-img.jpg')
    tags = TaggableManager()
    def __str__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length = 60,null = True, blank = True)
    company = models.CharField(max_length = 60,null = True, blank = True)
    rating = models.FloatField(max_length = 5)
    image = models.ImageField(upload_to = 'images/testimonials/' , default= 'static/images/courses/no-img.jpg')
    short_content = models.TextField(null = True, blank = True)
    date = models.DateField(blank=True)
    video = EmbedVideoField()  # same like models.URLField()
    tags = TaggableManager()
    def __str__(self):
        return self.name
