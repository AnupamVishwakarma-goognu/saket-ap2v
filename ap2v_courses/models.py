# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from home.models import Category
from django.template.defaultfilters import slugify
from core.models import SEOBaseModel
from courses.models import Courses as Anquira_Courses
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField


class Courses(SEOBaseModel):
    course_name = models.CharField(max_length=200, null=True, blank=True,default=None)
    short_name = models.CharField(max_length=200, null=False, blank=False,default=None)
    name = models.CharField(max_length=150, null=False, blank=False)
    home_banner_name = models.CharField(max_length=150, null=False, blank=True)
    slug = models.CharField(blank=True, unique=True, max_length=255)
    course_icon = models.ImageField(upload_to='images/courses/', default='images/courses/logo.png')
    banner_text = RichTextUploadingField()
    # content_heading=models.CharField(max_length=1000, null=False, blank=False,default = 'Decription2 Heading Here......Type')
    benefits = RichTextUploadingField(default = 'Benifit for this Course is Here............')
    description=RichTextUploadingField(default = 'Details of Description2 ......')
    price = models.IntegerField(null=False)
    actual_price = models.IntegerField(null=False)
    duration = models.CharField(max_length=10,null=False)
    recording_price = models.IntegerField(null=False,default=0)
    category_name = models.ManyToManyField(Category)
    rating = models.FloatField(null=False, blank=True)
    review_count=models.BigIntegerField(default=0, null=False, blank=False)
    related_courses = models.ManyToManyField("self", blank=True)
    tags=TaggableManager()
    show_on_site = models.BooleanField("Show course", default=True)
    contact_person = models.CharField(max_length=50,null=False)
    mobile = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=20, null=False)
    photo = models.ImageField(upload_to='images/courses/', default='static/images/courses/no-img.jpg')
    banner_display = models.BooleanField(default=False, null=False, help_text="Showing this course on top tab | default is False")
    featured = models.BooleanField(default=False, null=False)
    # skills  = models.TextField(null=False, blank=False,default = "Skill1,Skill2,Skill3,Skill4,Skill5,Skill6")
    benefits = RichTextUploadingField(default = 'Benifit for this Course is Here............')
    certificate_image = models.FileField(upload_to='images/', null=True,default = 'images/course-detail/certificate.jpg', blank=True)
    trending = models.BooleanField(default=False, null=False)
    anquira_course = models.ForeignKey(Anquira_Courses, default=139, related_name='anquira_courses',on_delete=models.DO_NOTHING)
    introduction_video = models.CharField(max_length=250,null=True,blank=True, default=None)
    pre_requirements = models.CharField(max_length=250,null=True,blank=True, default=None)
    active_inactive = models.BooleanField(null=True, blank=True, default=True)
    

    #def save(self, *args, **kwargs):
    #    self.slug=slugify(self.name)
    #    super(Courses, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        from core.views import check_duplicate_image
        course_icon_res = check_duplicate_image(self.course_icon)
        photo_res = check_duplicate_image(self.photo)
        certificate_image_res = check_duplicate_image(self.certificate_image)
        self.course_icon = course_icon_res['name']
        self.photo = photo_res['name']
        self.certificate_image = certificate_image_res['name']
        super(Courses, self).save(*args, **kwargs)

    def __str__(self):
            return self.name
        
def get_url_slug(self):
        return self.slug

class Offers(models.Model):
    added_on = models.DateTimeField(auto_now_add=True,help_text="Leave it blank",null=True)
    title = models.CharField(max_length=100)
    courses = models.ManyToManyField(Courses)
    description = models.TextField(null =True, blank=True, default=None)
    price=models.IntegerField(null=False)
    valid_till = models.DateField(null=True, blank=True,default=None)
    class Meta:
        verbose_name_plural="offers"
    def __str__(self):
        return self.title

class Lessons(models.Model):
    course=models.ForeignKey(Courses, related_name='courses',on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=50, null=False, blank=False)
    index=models.IntegerField(null=False)
    description=RichTextUploadingField()
    duration=models.CharField(max_length=10, null=False, blank=False, help_text="in minute")
    requirments = models.CharField(max_length=10000, null=False, blank=False, default="Requirements For this Course is Here...")
    preview_link = models.CharField(max_length=250, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="lessons"

class Courses_QnA(models.Model):
    course=models.ForeignKey(Courses, on_delete=models.PROTECT)
    question=models.TextField(null=False, blank=False)
    answer=models.TextField(null=False, blank=False)

    def __str__(self):
        return "Course: {c_name}, {q_title}".format(c_name=self.course, q_title=self.question)
    class Meta:
        verbose_name_plural="Course QnA"

class Locations(models.Model):
	name = models.CharField(max_length = 50, null=False, blank=False)
	local = models.BooleanField(null=False, blank=False, default=False)

	def __str__(self):
		return "{} ({})".format(self.name, self.local)

class RemoteItems(models.Model):
	title = models.CharField(max_length = 200, null=False, blank=False)
	link = models.URLField(null=False, blank=False)
	location = models.ForeignKey(Locations,on_delete=models.DO_NOTHING)

	def __str__(self):
		return "{} ({})".format(self.title, self.location.name)

class Industry_Projects(models.Model):
	belong_course 		= models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
	heading 			= models.CharField(max_length = 2000, null=False, blank=False)
	description 		= models.CharField(max_length = 10000, null=False, blank=False)

class Course_FQA(models.Model):
	belong_course 		= models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
	frequently_question = models.CharField(max_length = 1000, null=False, blank=False)
	answer				= models.CharField(max_length = 8000, null=False, blank=False)


class City(models.Model):
    name = models.CharField(blank=True, unique=True, max_length=255)
    slug = models.CharField(blank=True, unique=True, max_length=255)
    breadcrumb = models.CharField(max_length=200, null=False, blank=False, default="Breadcrumb")
    geo_placename = models.CharField(blank=True, unique=False, max_length=255, help_text="Generate using https://www.geo-tag.de/generator/en.html")
    geo_region = models.CharField(blank=True, unique=False, max_length=255, help_text="Generate using https://www.geo-tag.de/generator/en.html")
    geo_position = models.CharField(blank=True, unique=False, max_length=255, help_text="Generate using https://www.geo-tag.de/generator/en.html")
    geo_icbm = models.CharField(blank=True, unique=False, max_length=255, help_text="Generate using https://www.geo-tag.de/generator/en.html")
    image = models.FileField(upload_to='images/', null=True,default = None, blank=True)

    def __str__(self):
        return "{} ({})".format(self.name,self.slug)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        from core.views import check_duplicate_image
        dup_result = check_duplicate_image(self.image)
        self.image = dup_result['name']
        super(City, self).save(*args, **kwargs)


#class City_Specific_Course(models.Model):
class City_Specific_Course(SEOBaseModel):
    name = models.CharField(max_length=150, null=False, blank=False)
    slugs = models.CharField(blank=True, unique=True, max_length=255)
    course = models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    banner_text = RichTextUploadingField(default='Please mention course summary here.')
    description = RichTextUploadingField(default='Please mention course description here.')
    benefits = RichTextUploadingField(default='Please mention course benefits here.')
    city_specific_requirements = models.CharField(max_length=10000, null=False, blank=False, default="Pls mention the requirements of this course.")
    city = models.ForeignKey(City,on_delete=models.DO_NOTHING, blank = True, null = True )
    active_inactive = models.BooleanField(null=True, blank=True, default=True)
    show_tranding_in_footer = models.BooleanField(null=True, blank=True, default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        title = settings.CITY_COURSES_META_TITLE
        keyword = settings.CITY_COURSES_META_KEYWORDS
        description = settings.CITY_COURSES_META_DESCRIPTION

        name = self.city.name
        course = self.course.short_name
        course=course.rstrip(' Online')

        title = title.replace("<Course Name>", course)
        title = title.replace("<City>", name)

        description = description.replace("<Course Name>", course)
        description = description.replace("<City>", name)

        keyword = keyword.replace("<Course>", course)
        keyword = keyword.replace("<City>", name)

        if not self.title:
            self.title = title
        if not self.meta_description:
            self.meta_description = description
        if not self.meta_keyword:
            self.meta_keyword = keyword

        super(City_Specific_Course, self).save(*args, **kwargs)

class CitySpecificCoursesFQA(models.Model):
	belong_city_spqcific_course  = models.ForeignKey(City_Specific_Course,on_delete=models.DO_NOTHING)
	frequently_question = models.CharField(max_length = 1000, null=False, blank=False)
	answer = models.CharField(max_length = 8000, null=False, blank=False)


class OnlineContentRelatedCourse(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    content_related_online_courses = models.ManyToManyField(Courses, blank=True, related_name="content_online")
    content_related_city_courses = models.ManyToManyField(City_Specific_Course, blank=True, related_name="content_city")

class CityContentRelatedCourse(models.Model):
    city_course = models.ForeignKey(City_Specific_Course,on_delete=models.DO_NOTHING)
    content_related_online_courses = models.ManyToManyField(Courses, blank=True, related_name="content_online_related")
    content_related_city_courses = models.ManyToManyField(City_Specific_Course, blank=True, related_name="content_city_related")
     