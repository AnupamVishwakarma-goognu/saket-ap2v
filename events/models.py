# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime ,date 
from taggit.managers import TaggableManager
from location_field.models.plain import PlainLocationField
from home.models import Category





# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length = 40, null = True, blank = True)
    address = models.TextField(null = True, blank = True)
    phone = models.CharField(max_length = 40,null = True, blank = True)
    website = models.URLField(null = True, blank = True)
    city = models.CharField(max_length=255)
    location_map=models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['location_map'], zoom=7) 
    def __str__(self):
        return self.name
    
class Events(models.Model):
    name = models.CharField(max_length = 40, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    date = models.DateField(blank = True) 
    start_time  = models.TimeField( blank = True)    
    end_time = models.TimeField(blank =True)
    image=models.ImageField(upload_to = 'images/events', default = None)
    categories = models.ForeignKey(Category, null=True,blank=True,on_delete=models.SET_NULL)
    tags = TaggableManager()
    contact_name = models.CharField(max_length = 40, null = True, blank = True)
    contact_number = models.CharField(max_length = 40,null = True, blank = True)
    contact_email = models.EmailField(max_length = 255,null = True, blank = True)
    venue = models.ForeignKey(Venue, null=True,blank=True,on_delete=models.SET_NULL,related_name='venue')
    def __str__(self):
        return self.name

