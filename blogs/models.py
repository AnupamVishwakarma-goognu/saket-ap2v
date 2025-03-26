# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from statistics import mode
from unicodedata import category

from django.db import models
from datetime import datetime,date
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from home.models import Category, Author
from django.template.defaultfilters import slugify
from core.models import SEOBaseModel
import random
from ap2v_courses.models import City

from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Blogs(SEOBaseModel):
	CATEGORY_TYPE = (
            ('1', 'Blog'),
            ('2', 'Question-Answare')
    )
	# type = models.CharField(max_length=300, choices = CATEGORY_TYPE, null= True)
	title=models.CharField(max_length=50,null=False,blank=False)
	slug = models.SlugField(blank=True)
	content=RichTextField()
	tags=TaggableManager()
	categories=models.ForeignKey(Category, related_name='comments',on_delete=models.DO_NOTHING)
	author=models.ForeignKey(Author,on_delete=models.DO_NOTHING)
	published_on=models.DateField(default=datetime.now,blank=True)
	show_on_site = models.BooleanField("published_alllow", default=False)
	image=models.ImageField(upload_to='images/blogs/',default="images/blog_default_image.jpeg")
	views = models.IntegerField(null=True,blank=True)
	city=models.ForeignKey(City,on_delete=models.DO_NOTHING,default = None, null=True, blank=True)

	def save(self, *args, **kwargs):
			self.slug = slugify(self.title)
			self.views = random.randint(100,999)
			super(Blogs, self).save(*args, **kwargs)
	def __str__(self):
		return self.title
	class Meta:
		verbose_name_plural="blogs"


class Comments(models.Model):
    post = models.ForeignKey(Blogs, related_name='comments',on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Author,on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    approved_comment = models.BooleanField(default=False)



class BlogNewsEmails(models.Model):
	date = models.DateTimeField(default=datetime.now,blank=True)
	email = models.CharField(max_length=50,null=False,blank=False)

class InterviewQuestionTitleDescription(SEOBaseModel):
	title=models.CharField(max_length=50,null=False,blank=False)
	slug = models.SlugField(blank=True)
	content=RichTextField()
	tags=TaggableManager()
	categories=models.ForeignKey(Category, related_name='blong_cate',on_delete=models.DO_NOTHING)
	image=models.ImageField(upload_to='images/interview_question/',default="images/blog_default_image.jpeg")
	views = models.IntegerField(null=True,blank=True)

	def __str__(self):
		return self.title
	
	@property
	def get_total_question(self):
		# print("***************************")
		# print(self.id)
		question_ans_obj = QuestionAnswer.objects.filter(question_title = self.id).count()
		return question_ans_obj
	

class QuestionAnswer(models.Model):
	CATEGORY_TYPE = (
            ('1', 'Beginner'),
            ('2', 'Advance')
    )
	date = models.DateField(auto_now_add=True)
	type = models.CharField(max_length=300, choices = CATEGORY_TYPE, null= True)
	# blog = models.ForeignKey(Blogs,on_delete=models.DO_NOTHING)
	question_title = models.ForeignKey(InterviewQuestionTitleDescription,on_delete=models.DO_NOTHING,default=None)
	index = models.IntegerField(null=True,blank=True, default=0)
	question = models.TextField(null=False, blank=False)
	answer = RichTextUploadingField()