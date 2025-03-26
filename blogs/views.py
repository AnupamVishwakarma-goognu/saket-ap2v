# from django.shortcuts import render
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django.db.models import Count
from django.shortcuts import render ,get_object_or_404
from .models import Blogs ,Comments,BlogNewsEmails, QuestionAnswer,InterviewQuestionTitleDescription
from home.models import Category, Configrations
from django.conf import settings
from django.http import Http404
from ap2v_courses.models import Courses
from learning_paths.models import Learning_Path
from django.http import JsonResponse
# Create your views here.
#live_configration_id = settings.LIVE_CONFIGRATION_ID
#configration = Configrations.objects.filter(id=live_configration_id)

def all_blogs(request):
	blogs = Blogs.objects.order_by('-published_on')
	return render(request, 'blogs/blogs_listing.html', {'blogs': blogs})

def display_blog(request, slug):
	blog_details = Blogs.objects.filter(slug=slug)
	if blog_details.exists():
		comments=Comments.objects.filter(post=blog_details.first()).all()
		count=Comments.objects.filter(post=blog_details.first()).count()
	else:
		raise Http404('page not found')
	return render(request, 'blogs/blog_details.html', {'blog_details': blog_details.first(),'comments':comments,'count':count})





def listing(request):
	ctx={}
	# ctx['category_all'] = Category.objects.all()
	ctx['category_popular'] = Category.objects.all()[:4]
	ctx['tranding_course_footer'] = Courses.objects.filter(trending = True,active_inactive=True)
	ctx['tranding_course'] = Courses.objects.filter(trending = True,active_inactive=True)
	ctx['listing_path_footer'] = Learning_Path.objects.filter(trending = True)

	ctx['blogs'] = Blogs.objects.filter(show_on_site = True).order_by('-published_on')

	popular_blog = Blogs.objects.all().order_by("-views")
	ctx['popular_blog']=popular_blog

	return render(request, 'blogs/listing.html', ctx)

def listing_city_blog(request,slug):
	ctx={}
	# print(slug)
	# print("------------------------------------------------------------")
	# ctx['category_all'] = Category.objects.all()
	ctx['category_popular'] = Category.objects.all()[:4]
	ctx['tranding_course_footer'] = Courses.objects.filter(trending = True,active_inactive=True)
	ctx['tranding_course'] = Courses.objects.filter(trending = True,active_inactive=True)
	ctx['listing_path_footer'] = Learning_Path.objects.filter(trending = True)

	ctx['blogs'] = Blogs.objects.filter(city__name=slug).order_by('-published_on')

	popular_blog = Blogs.objects.all().order_by("-views")
	ctx['popular_blog']=popular_blog

	return render(request, 'blogs/listing.html', ctx)

def display(request,slug):
	ctx={}
	blog_details = Blogs.objects.filter(slug=slug).first()
	if not blog_details:
		return render(request,'v4_home/error_course_not_found.html',status=404)
	ctx['blog_details']=blog_details

	previous_blog = Blogs.objects.filter(id = blog_details.id-1).first()
	ctx['previous_blog']=previous_blog

	next_blog = Blogs.objects.filter(id = blog_details.id+1).first()
	ctx['next_blog']=next_blog

	ctx['category_all'] = Category.objects.all()
	ctx['tranding_course_footer'] = Courses.objects.filter(trending = True,active_inactive=True)
	ctx['listing_path_footer'] = Learning_Path.objects.filter(trending = True)

	list_tag = []
	for i in blog_details.tags.all():
			list_tag.append(i.slug)
	related_course_list = Courses.objects.filter(tags__slug__in=list_tag,active_inactive=True).distinct()
	ctx['related_course_list'] = related_course_list

	popular_blog = Blogs.objects.all().order_by("-views")
	ctx['popular_blog']=popular_blog

	ctx['category_popular'] = Category.objects.all()[:4]

	# blog_qa_obj = QuestionAnswer.objects.filter(blog_id = blog_details.id)
	# print(blog_qa_obj)
	# ctx['blog_qa_obj']=blog_qa_obj

	category = blog_details.categories
	

	cour_obj  =Courses.objects.filter(category_name = category.id).first()
	ctx['cour_obj'] = cour_obj


	return render(request, 'blogs/display.html', ctx)

def subscribenewslatter(request):
	email = request.GET.get("email",None)
	print(email)
	if email:
		if BlogNewsEmails.objects.filter(email=email).exists():
			return JsonResponse({"messages":"You already subscribed our news latter."},status=200)
		else:
			x = BlogNewsEmails(
				email=email
			)
			x.save()
			return JsonResponse({"messages":"You subscribed our news latter."},status=200)
	return JsonResponse({"messages":"Internal server error."},status=201)



def interview_questions_listing(request):
	ctx={}
	ctx['category_all'] = Category.objects.all()
	# ctx['category_popular'] = Category.objects.all()[:4]
	# ctx['tranding_course_footer'] = Courses.objects.filter(trending = True,active_inactive=True)
	# ctx['tranding_course'] = Courses.objects.filter(trending = True,active_inactive=True)
	# ctx['listing_path_footer'] = Learning_Path.objects.filter(trending = True)

	# ctx['blogs'] = Blogs.objects.filter(type=2).order_by('-published_on')

	# popular_blog = Blogs.objects.filter(type=2).order_by("-views")
	# ctx['popular_blog']=popular_blog


	question_answer_title_obj = InterviewQuestionTitleDescription.objects.all()
	ctx['question_answer_title_obj']=question_answer_title_obj
	return render(request, 'blogs/interview_question_listing.html', ctx)

def interview_questions_display(request,slug):
	ctx={}
	# blog_details = Blogs.objects.filter(slug=slug).first()
	# ctx['blog_details']=blog_details

	# previous_blog = Blogs.objects.filter(id = blog_details.id-1).first()
	# ctx['previous_blog']=previous_blog

	# next_blog = Blogs.objects.filter(id = blog_details.id+1).first()
	# ctx['next_blog']=next_blog

	# ctx['category_all'] = Category.objects.all()
	# ctx['tranding_course_footer'] = Courses.objects.filter(trending = True,active_inactive=True)
	# ctx['listing_path_footer'] = Learning_Path.objects.filter(trending = True)

	# list_tag = []
	# for i in blog_details.tags.all():
	# 		list_tag.append(i.slug)
	# related_course_list = Courses.objects.filter(tags__slug__in=list_tag,active_inactive=True).distinct()
	# ctx['related_course_list'] = related_course_list

	# popular_blog = Blogs.objects.all().order_by("-views")
	# ctx['popular_blog']=popular_blog

	# ctx['category_popular'] = Category.objects.all()[:4]

	# blog_qa_obj = QuestionAnswer.objects.filter(blog_id = blog_details.id)
	# print(blog_qa_obj)
	# ctx['blog_qa_obj']=blog_qa_obj

	question_answer_title_obj = InterviewQuestionTitleDescription.objects.filter(slug = slug).first()
	ctx['question_answer_title_obj']=question_answer_title_obj

	all_interview_questions = QuestionAnswer.objects.filter(question_title__slug = slug)
	ctx['all_interview_questions']=all_interview_questions
	
	question_answer_obj_beginner = QuestionAnswer.objects.filter(question_title__slug = slug, type = 1)
	ctx['question_answer_obj_beginner']=question_answer_obj_beginner
	question_answer_obj_beginner_count = QuestionAnswer.objects.filter(question_title__slug = slug, type = 1).count()
	ctx['question_answer_obj_beginner_count']=int(question_answer_obj_beginner_count)/4


	question_answer_obj_advance = QuestionAnswer.objects.filter(question_title__slug = slug, type = 2)
	ctx['question_answer_obj_advance']=question_answer_obj_advance
	question_answer_obj_advance_count = QuestionAnswer.objects.filter(question_title__slug = slug, type = 2).count()
	ctx['question_answer_obj_advance_count']=question_answer_obj_advance_count

	ctx['question_count'] = QuestionAnswer.objects.filter(question_title__slug = slug).count()

	related_question_topic = InterviewQuestionTitleDescription.objects.filter(categories = question_answer_title_obj.categories).exclude(slug=slug)
	ctx['related_question_topic']=related_question_topic

	course_show = settings.SHOW_COURSE_COURSEL
	ctx['course_show']=course_show

	print(question_answer_title_obj)
	category_obj = Category.objects.filter(slug=question_answer_title_obj.categories.slug)
	print(category_obj)
	category_courses = Courses.objects.filter(category_name = category_obj.first(),active_inactive=True)
	ctx['category_courses']=category_courses
	print(category_courses)

	banner_courses = Courses.objects.filter(category_name = category_obj.first(),active_inactive=True).first()
	ctx['banner_courses']=banner_courses
	print(banner_courses)



	return render(request, 'blogs/interview_question_details.html', ctx)


def category(request,slug):
    ctx={}
    # print('09'*100)
    # print(slug)
    blog_category = Blogs.objects.filter(categories__slug=slug,show_on_site = True).all()
    # print(blog_category)
    ctx['tranding_course'] = Courses.objects.filter(trending = True,active_inactive=True)
    ctx['blog_category']=blog_category
	
    return render(request, 'blogs/category_blog.html', ctx)

def tags_blog(request,slug):
    ctx={}
    print(slug)
    tag=[]
    tag.append(slug)
    blog_category = Blogs.objects.filter(tags__name__in=tag,show_on_site = True).all()
    print(blog_category)
    ctx['tranding_course'] = Courses.objects.filter(trending = True,active_inactive=True)
    ctx['blog_category']=blog_category
	
    return render(request, 'blogs/tags_blog.html', ctx)