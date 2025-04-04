# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import datetime


# Create your models here.

class Refer_and_Earn(models.Model):
    candidate_name = models.CharField(max_length=30)
    candidate_phone = models.BigIntegerField(default=0)
    candidate_exists = models.BooleanField(default=False)
    friend_name = models.CharField(max_length=30)
    friend_phone = models.BigIntegerField(default=0)
    friend_email = models.EmailField()
    friend_designation = models.CharField(max_length=50)

    def __str__(self):
        return "Candidate Name: {c_name}, Friend Name: {f_name}, Friend Email: {f_email}".format(
            c_name=self.candidate_name, f_name=self.friend_name, f_email=self.friend_email)

    class Meta:
        verbose_name_plural = "Refer And Earn"


class Category(models.Model):
    index = models.IntegerField(null=True, blank=True, default=0)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    display_home = models.BooleanField(default=False, blank=True, help_text="To display on this category on home page.")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('display_category', kwargs={'category_slug': str(self.slug)})


class SidebarCategory(models.Model):
    batch_span = models.ManyToManyField(Category)
    title = models.CharField(max_length=50, null=False)
    batches = models.CharField(max_length=50, null=False)
    details = RichTextField()

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    designation = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='media/images/author/')

    def __str__(self):
        return self.name


class Configrations(models.Model):
    company_name = models.CharField(max_length=32, null=False, blank=False)
    email = models.EmailField(max_length=70, blank=False, null=False, unique=True)
    mobile = models.CharField(max_length=50, null=False, blank=False)
    landline = models.CharField(max_length=50, null=False, blank=False)
    events_header_text = models.TextField(max_length=2000, null=False, blank=True)
    testimonials_header_text = models.TextField(max_length=2000, null=False, blank=True)
    blogs_header_text = models.TextField(max_length=2000, null=False, blank=True)
    courses_header_text = models.TextField(max_length=2000, null=False, blank=True)
    gallary_header_text = models.TextField(max_length=2000, null=False, blank=True)
    contect_us_header_text = models.TextField(max_length=2000, null=False, blank=True)

    def __str__(self):
        return self.company_name


class Location(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    address = models.CharField(max_length=500, null=False, blank=False)
    phone = models.CharField(max_length=500, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


# class Enquiry(models.Model):
#     page_source = models.CharField(max_length=1000, null=True, blank=True)
#     name = models.CharField(max_length=100, null=True, blank=True)
#     phone = models.CharField(max_length=15, null=True, blank=True)
#     email = models.CharField(max_length=100, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.name


class FeaturedCertifications(models.Model):
    certification_text = models.CharField(max_length=200, null=False, blank=False, help_text="Certification in Python")
    certificate_image = models.FileField(upload_to='images/', null=True, default='certificate.jpg', blank=True)
