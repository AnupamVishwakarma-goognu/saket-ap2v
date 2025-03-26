# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ap2v_courses.models  import Courses, City, City_Specific_Course
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from core.models import SEOBaseModel

# Create your models here.

class Learning_Path(SEOBaseModel):
    slug = models.CharField(blank=False, max_length=255, unique=True)
    heading = models.CharField(blank=False, unique=False, max_length=255)
    description	= RichTextField(default = 'Deatils of Description')
    preview_video_link = models.CharField(blank=False, unique=False, max_length=255)
    banner_image = models.ImageField(upload_to = 'images' , default= 'static/images/courses/no-img.jpg')
    small_svg_image_for_home = models.FileField(upload_to = 'images' , default= '')
    trending = models.BooleanField(default=False)
    banner_display = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from core.views import check_duplicate_image
        banner_image_res = check_duplicate_image(self.banner_image)
        small_svg_image_for_home_res = check_duplicate_image(self.small_svg_image_for_home)
        
        self.banner_image = banner_image_res['name']
        self.small_svg_image_for_home = small_svg_image_for_home_res['name']
        super(Learning_Path, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.heading

class Learning_Path_Courses(models.Model):
    index = models.IntegerField(blank=False, unique=False)
    courses = models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    learning_path = models.ForeignKey(Learning_Path,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.learning_path.heading



class City_Specific_Learning_Path(SEOBaseModel):
    parent_learning_path = models.ForeignKey(Learning_Path,on_delete=models.DO_NOTHING)
    slug = models.CharField(blank=True, max_length=255, unique=True)
    heading = models.CharField(blank=False, max_length=255)
    description = RichTextField()
    city = models.ForeignKey(City,on_delete=models.DO_NOTHING, blank = False, null = False )
    show_tranding_in_footer = models.BooleanField(null=True, blank=True, default=False)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.heading)
        super(City_Specific_Learning_Path, self).save(*args, **kwargs)

    def __str__(self):
        return self.heading
