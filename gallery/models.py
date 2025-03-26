# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Gallery(models.Model):
	name=models.CharField(max_length=50,null=False,blank=False)
	description=models.CharField(max_length=300,null=False,blank=False)
	photo=models.ImageField(upload_to ='images/gallery/')
	def __str__(self):
		return self.name
	
