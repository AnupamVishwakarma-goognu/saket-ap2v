# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ap2v_courses.models import Courses
from core.models import SEOBaseModel

# Create your models here.

class Meta(SEOBaseModel):
    uri = models.CharField(max_length=255, null=False, blank=True, unique=True)

    def __str__(self):
        if self.uri:
            return "{}".format(self.uri)

        return '/'

    def save(self, *args, **kwargs):
        if self.uri != "/":
            self.uri = self.uri.rstrip("/")
        super(Meta, self).save(*args, **kwargs)


class SkillsContent(models.Model):
    heading = models.CharField(max_length=200, null=True, blank=True, default="Page Title")
    discription = models.TextField(null=True, blank=True,)
    uri = models.CharField(max_length=255, null=False, blank=True, unique=True)

    def __str__(self):
        if self.uri:
            return "{}".format(self.uri)

        return '/'

    def save(self, *args, **kwargs):
        if self.uri != "/":
            self.uri = self.uri.rstrip("/")
        super(SkillsContent, self).save(*args, **kwargs)
