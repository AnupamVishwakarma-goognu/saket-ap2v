from ast import Try
from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from ap2v_courses.models import Courses, Offers, TaggableManager, Lessons, Industry_Projects, Course_FQA, City_Specific_Course,City
from home.models import Category
from django.views.generic import TemplateView
from testimonials.models import Text, Video
from home.models import Configrations
from django.conf import settings
from django.http import Http404, HttpResponse
from taggit.models import Tag
from itertools import chain
from django.views.generic import View, TemplateView
# from .filters import (
#     SearchDataFilter
# )
from testimonials.models import Text



def learning_path_listing(request):
    ctx={}
    listing_path_queryset = Learning_Path.objects.all().order_by('id')
    ctx['listing_path_queryset']=listing_path_queryset
    
    return render(request,'v4_courses/learning-path-listing.html',ctx)

def learning_path_details(request, slug):
    ctx={}

    testimonials = Text.objects.all()
    course_tag_queryset = Courses.tags.all()
    ctx['testimonials'] = testimonials
    ctx['course_tag_queryset'] = course_tag_queryset
    ctx['category_all'] = Category.objects.all()

    listing_path_all = Learning_Path.objects.all().order_by('id')
    ctx['listing_path_all'] = listing_path_all

    ctx['courses'] = []

    if Learning_Path.objects.filter(slug = slug).exists():
        listing_path_queryset = Learning_Path.objects.get(slug = slug)

        lp_courses = Learning_Path_Courses.objects.filter(learning_path = listing_path_queryset.id).order_by('index')
        lp_id = Learning_Path.objects.get(slug = slug).id

        city_specific_learning_path_queryset = City_Specific_Learning_Path.objects.filter(parent_learning_path=lp_id)

        # ??
        ctx['city_specific_learning_path_queryset'] = city_specific_learning_path_queryset

        ctx['heading'] = listing_path_queryset.heading
        ctx['description'] = listing_path_queryset.description
        ctx['banner_image'] = listing_path_queryset.banner_image
        ctx['preview_video_link'] = listing_path_queryset.preview_video_link
        ctx['slug']=slug

        for lp_course in lp_courses:
            tmp_d = {}
            tmp_d['name'] = lp_course.courses.name
            tmp_d['slug'] = lp_course.courses.slug
            tmp_d['description'] = lp_course.courses.description
            tmp_d['tags'] = lp_course.courses.tags
            tmp_d['photo'] = lp_course.courses.photo
            tmp_d['course_icon'] = lp_course.courses.course_icon
            tmp_d['banner_text'] = lp_course.courses.banner_text

            ctx['courses'].append(tmp_d)

        """
        list_tag = []
        for j in ctx['courses']:
            for i in j.courses.tags.all():
                    list_tag.append(i.slug)
        related_course_list = Courses.objects.filter(tags__slug__in=list_tag).distinct()
        ctx['related_course_list'] = related_course_list
        """

        return render(request,'v4_courses/learning-path-detail.html',ctx)
                                                                      

    elif City_Specific_Learning_Path.objects.filter(slug = slug).exists():
        plp_obj = City_Specific_Learning_Path.objects.get(slug = slug).parent_learning_path
        lp_obj = City_Specific_Learning_Path.objects.get(slug=slug)

        ctx['heading'] = lp_obj.heading
        ctx['description'] = lp_obj.description
        ctx['banner_image'] = plp_obj.banner_image
        ctx['slug']=slug

        plp_courses = Learning_Path_Courses.objects.filter(learning_path=plp_obj).values_list('courses')
        lp_courses = City_Specific_Course.objects.filter(course__id__in=[plp_courses],city=lp_obj.city)

        for lp_course in lp_courses:
            tmp_d = {}
            tmp_d['name'] = lp_course.name
            tmp_d['slug'] = lp_course.slugs
            tmp_d['description'] = lp_course.banner_text
            tmp_d['tags'] = lp_course.course.tags
            tmp_d['photo'] = lp_course.course.photo
            tmp_d['course_icon'] = lp_course.course.course_icon
            tmp_d['banner_text'] = lp_course.banner_text

            ctx['courses'].append(tmp_d)
        
        city_specific_learning_path_queryset = City_Specific_Learning_Path.objects.filter(parent_learning_path=plp_obj.id)
        print(city_specific_learning_path_queryset)
        # print("--------------------------------==========================================================")
        # ctx['city_specific_learning_path_queryset'] = city_specific_learning_path_queryset

        return render(request,'v4_courses/learning-path-detail.html',ctx)
    
    else:
        return render(request,'v4_home/error_course_not_found.html',status=404)

def city_learning_paths(request,city_lp=None):
    print(city_lp)
    ctx={}
    city_learning_paths = City_Specific_Learning_Path.objects.filter(city__name = city_lp)
    ctx['listing_path_queryset']=city_learning_paths
    ctx['city_lp'] = city_lp
    return render(request,'v4_courses/learning-path-listing.html',ctx)