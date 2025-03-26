# from __future__ import unicode_literals

from __future__ import print_function
from django.shortcuts import render , get_object_or_404, redirect
from .models import Courses, Offers, TaggableManager, Lessons, Industry_Projects, Course_FQA, City_Specific_Course,City, CitySpecificCoursesFQA,OnlineContentRelatedCourse,CityContentRelatedCourse
from home.models import Category
from django.views.generic import TemplateView
from testimonials.models import Text, Video
from home.models import Configrations
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from taggit.models import Tag
from itertools import chain
from django.views.generic import View, TemplateView
from .filters import (
    SearchDataFilter
)
# ---------------Landing page import models-------------------------
from landing_page.models import Landing_Page, SoftwareTools, ExamCertification, Projects, Testimonial
from django.views.decorators.csrf import csrf_exempt
import requests
import json, ast
from learning_paths.models import Learning_Path
from enquiries.views import create_enquiry_api
from communication.models import CounselorContactNumber
from datetime import timedelta,date




# Create your views here.

#live_configration_id = settings.LIVE_CONFIGRATION_ID
#configration = Configrations.objects.filter(id=live_configration_id)

# views for courses
def all_courses(request):
    ctx={}
    category_queryset = Category.objects.all()[:8]
    ctx['category_queryset'] = category_queryset
    courses = Courses.objects.order_by('-price')
    ctx['courses'] = Courses.objects.filter(active_inactive=True).order_by('-price')

    return render(request, 'v4_courses/course-listing.html', ctx)

def all_coursesCity(request,city_course=None):
    # print("444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444")
    print(city_course)
    ctx={}
    ctx['courses'] = City_Specific_Course.objects.filter(city__name=city_course)
    ctx['city_course'] = True
    ctx['city_name'] = city_course
    category_queryset = Category.objects.all()[:8]
    ctx['category_queryset'] = category_queryset

    return render(request, 'v4_courses/course-listing.html', ctx)

class CoursesDynamicTemplateView(TemplateView):
    template_name = "v4_courses/course-detail.html"
    

    def get_context_data(self, *args, **kwargs):
        if Courses.objects.filter(slug = self.kwargs.get('slug'),active_inactive=True).exists():
            context={}
            courses_slug = Courses.objects.filter(slug=self.kwargs.get('slug'))
            if courses_slug.exists():
                context['course_details'] = courses_slug.first()
                context['lessons'] = Lessons.objects.filter(course=courses_slug.first()).order_by('index')[:6]
                context['count'] = Lessons.objects.filter(name=courses_slug.first()).count()
                context['projects'] = Industry_Projects.objects.filter(belong_course=courses_slug.first())
                context['fqa'] = Course_FQA.objects.filter(belong_course=courses_slug.first())
                context['city_name'] = City_Specific_Course.objects.filter(course=courses_slug.first())
                context['heading'] = context['course_details'].name
                context['trending_courses'] = Courses.objects.filter(trending=True,active_inactive=True).exclude(id=context['course_details'].id)
                context['testimonials'] = Text.objects.filter(course=courses_slug.first())

                list_tag = []
                for i in courses_slug.first().category_name.all():
                        list_tag.append(i.id)
                # print("---------------------------------------------------------------------------------------------")
                # print(list_tag)
                # print(courses_slug.first().category_name)
                # print(Courses.objects.filter(category_name__in=list_tag))
                # print(Courses.objects.filter(category_name__in=list_tag).count())
                # print(Courses.objects.filter(category_name__in=list_tag).distinct())
                # print(Courses.objects.filter(category_name__in=list_tag).distinct().count())
                # related_course_list = Courses.objects.filter(tags__slug__in=list_tag).distinct()
                context['related_course_list'] = Courses.objects.filter(category_name__in=list_tag,active_inactive=True).distinct()
                context['course']=True
                context['anquira_course']=courses_slug.first().anquira_course.id

                context['data_status'] = 1 if context.get('course_details') else 0

                context['ccslug']=self.kwargs.get('slug')
                context['next_date'] = date.today()+timedelta(days=1)
                context['base_url'] = settings.BASE_URL
                online_re_obj = OnlineContentRelatedCourse.objects.filter(course=courses_slug.first())
                
                context['online_related'] = online_re_obj
                    


            return context

        elif City_Specific_Course.objects.filter(slugs = self.kwargs.get('slug'),active_inactive=True).exists():
            context={}
            courses_slug = Courses.objects.filter(slug=self.kwargs.get('slug'))
            a = City_Specific_Course.objects.get(slugs=self.kwargs.get('slug'))
            courses_slug = a.course.slug
            context['base_url'] = settings.BASE_URL

            try:
                # related_parent_course = Courses.objects.filter(id=a.id)
                # related_parent_course2 = Courses.objects.filter(id=a.id).first()

                # print("**************************************--------------------------------------------------------------------------------------------------------------------------------------------")
                # print(related_parent_course2.category_name.all())
                # rel_cou = Courses.objects.filter(category_name__in=related_parent_course2.category_name.all())
                # # print(rel_cou)
                # # list_tag = []
                # # for i in related_parent_course.first().tags.all():
                # #         list_tag.append(i.slug)
                # # related_course_list = Courses.objects.filter(tags__slug__in=list_tag).distinct()
                # context['related_course_list'] = rel_cou

                list_tag = []
                for i in Courses.objects.get(slug=a.course.slug).category_name.all():
                        list_tag.append(i.id)
                # print("---------------------------------------------------------------------------------------------")
                # print(list_tag)
                # print(Courses.objects.filter(category_name__in=list_tag))
                # print(Courses.objects.filter(category_name__in=list_tag).count())
                # print(Courses.objects.filter(category_name__in=list_tag).distinct())
                # print(Courses.objects.filter(category_name__in=list_tag).distinct().count())
                # context['related_course_list'] = Courses.objects.filter(category_name__in=list_tag).distinct()
                context['related_course_list'] = City_Specific_Course.objects.filter(course__category_name__in=list_tag,city=a.city,active_inactive=True)
            except Exception as e:
                print(e)

            context['course_details'] = Courses.objects.get(slug=a.course.slug)
            context['lessons'] = Lessons.objects.filter(course=a.course.id).order_by('index')[:6]
            context['count'] = Lessons.objects.filter(course=a.course.id).count()
            context['projects'] = Industry_Projects.objects.filter(belong_course=a.course.id)
            context['fqa'] = CitySpecificCoursesFQA.objects.filter(belong_city_spqcific_course=a.id)
            context['city_name'] = City_Specific_Course.objects.filter(course=a.course.id)
            context['city_specific'] = True
            context['city_specific_course'] = City_Specific_Course.objects.get(slugs=self.kwargs.get('slug'))
            context['heading'] = context['course_details'].name
            context['trending_courses'] = City_Specific_Course.objects.filter(course__trending=True,city=a.city, active_inactive=True).exclude(id=a.id)
            context['testimonials'] = Text.objects.filter(course=Courses.objects.get(slug=a.course.slug))
            category_all = Category.objects.all()

            # context['trending_course_footer'] = City_Specific_Course.objects.filter(course__trending=True,city=a.city)
            context['learning_path_footer'] = Learning_Path.objects.filter(trending=True)
            context['course']=True
            context['anquira_course']=Courses.objects.filter(slug=a.course.slug).first().anquira_course.id
            
            context['category_all']=category_all
            context['data_status'] = 1 if context.get('course_details') else 0

            context['ccslug']=self.kwargs.get('slug')
            context['next_date'] = date.today()+timedelta(days=1)
            context['base_url'] = settings.BASE_URL
            online_re_obj = CityContentRelatedCourse.objects.filter(city_course=a.id)
            context['online_related'] = online_re_obj
            
            return context
        
        # elif City.objects.filter(slug = self.kwargs.get('slug')).exists():
        #     # print(self.kwargs.get('slug'))
        #     context = {}

        #     context['courses'] = City_Specific_Course.objects.filter(city__name=self.kwargs.get('slug'))
        #     context['data_status'] = 1 if context.get('city_specific_course') else 0
        #     context['city_course'] = True
        #     category_queryset = Category.objects.all()[:8]
        #     context['category_queryset'] = category_queryset

        #     # print(context['courses'])
        #     # print(context['data_status'])
        #     context['data_status'] = 2

        #     return context
        else:
            context = {}
            context['data_status'] = 0
            return context


    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if context['data_status'] == 0:
            # raise Http404('page not found')
            # return render(self.request,'v4_home/error_course_not_found.html')
            from django.shortcuts import render_to_response
            response = render_to_response('v4_home/error_course_not_found.html')
            response.status_code = 404
            return response
        if context['data_status'] == 2:
            return render(self.request, 'v4_courses/course-listing.html', context)
        
        return render(self.request, self.template_name, context)



# ------------------------Landing page code------------------------

def landing_page(request,slug):

    landing_page_queryset = Landing_Page.objects.filter(slug = slug).first()

    if landing_page_queryset == None:
        return HttpResponse("<h1>404 Page Not Found</h1>")
    if landing_page_queryset:
        software_tools_queryset = SoftwareTools.objects.filter(belong_landing_page = landing_page_queryset.id)
        exam_certification_queryset = ExamCertification.objects.filter(belong_landing_page = landing_page_queryset.id).first()
        projects_queryset = Projects.objects.filter(belong_landing_page = landing_page_queryset.id)
        testimonial_queryset = Testimonial.objects.filter(belong_landing_page = landing_page_queryset.id)
        tranding_course_footer = Courses.objects.filter(trending = True,active_inactive=True)
        listing_path_footer = Learning_Path.objects.filter(trending = True)
    
    all_number = CounselorContactNumber.objects.all()


    return render(request, 'landing_page/landing-page.html',{'landing_page_queryset':landing_page_queryset,
                            'software_tools_queryset':software_tools_queryset, 'exam_certification_queryset':exam_certification_queryset,
                            'projects_queryset':projects_queryset, 'testimonial_queryset':testimonial_queryset,'tranding_course_footer':tranding_course_footer,
                            'listing_path_footer':listing_path_footer,'all_number':all_number})

@csrf_exempt
def enquirysave(request):
    if request.method == "POST":
        baseurl = request.build_absolute_uri()
        # print(baseurl)

        if not request.POST._mutable:
            request.POST._mutable = True
            request.POST['key'] = "CONNTOANQUIRA@3685"
        a = create_enquiry_api(request)
        if a.status_code == 200:
            return JsonResponse({"status" : 1}) 
        else:
            return JsonResponse({"status" : 0})

def display_category(request, category_slug, city_slug=False):
    ctx={}
    courses = []
    category_queryset = Category.objects.all()[:8]
    ctx['category_queryset'] = category_queryset
    #category_obj = Category.objects.filter(slug=category_slug).first()

    try:
        category_obj = Category.objects.get(slug=category_slug)
    except:
        #raise Http404('page not found')
        return redirect('/', permanent=True)

    if city_slug:
        filter_courses = City_Specific_Course.objects.filter(course__category_name=category_obj, city__slug=city_slug)
        if filter_courses:
            for i in filter_courses:
                dict = {}
                dict['id']=i.id
                dict['slug']=i.slugs
                dict['course_icon']=i.course.course_icon
                dict['name']=i.name
                dict['category_name']=i.course.category_name
                dict['rating']=i.course.rating
                dict['review_count']=i.course.review_count
                dict['banner_text']=i.banner_text
                courses.append(dict)
    else:
        filter_courses = Courses.objects.filter(category_name = category_obj,active_inactive=True)
        if filter_courses:
            for i in filter_courses:
                dict = {}
                dict['id']=i.id
                dict['slug']=i.slug
                dict['course_icon']=i.course_icon
                dict['name']=i.name
                dict['category_name']=i.category_name
                dict['rating']=i.rating
                dict['review_count']=i.review_count
                dict['banner_text']=i.banner_text
                courses.append(dict)

    # show 404 if no courses
    if len(filter_courses) <= 0:
        raise Http404('page not found')

    ctx['courses'] = courses
    ctx['category_name'] = category_obj
    return render(request, 'v4_courses/course-listing.html', ctx)
    
    # courses = Courses.objects.filter(category_name = category_obj.first())
    # return render(request, 'courses/category.html', {'courses': courses})

# views for offers.htm
def offers(request):
    offer_id = request.GET.get("offer_id",None)
    if offer_id:
        offers = Offers.objects.filter(id=offer_id)
        if not offers:
            return redirect("offers")
    else:
        offers = Offers.objects.all()
    return render(request, 'courses/offers.html', {'offers': offers})

# views for certification
def certifications(request):
	certification = Certifications.objects.order_by('-price')
	return render(request, 'courses/certifications.html', {'certification': certification})

# views for slugs based on CERTIFICATION model
def display_certification(request, slug):
        certification_details = Certifications.objects.get(slug=slug)
        return render(request, 'courses/detail_certifications.html', {'certification_details': certification_details})


def contact_enquiry(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        mobile = request.POST['mobile_number']
        email_address = request.POST['email_address']
        text_message = request.POST['text_message']
        #captcha_code = request.POST['captcha_code']
        message = """Name: %s
Email Address: %s
Mobile Number: %s
Message: %s
For location Gurgaon""" %(firstname,email_address,str(mobile),text_message)
    if True:
        try:
            request.session['enquiry_sumited'] = True
            enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['bhart@goognu.com', 'ashutosh@ap2v.com', 'ravi@ap2vgurgaon.training'])
            enquiry_mail_obj.send()
            return redirect('thankyou')
        except Exception as e:
            print(e, "this is error")
            return JsonResponse({"result": e}, status=444)
    else:
            return JsonResponse({"result": False}, status=404)


#for send enquiry through mail for download course content
def contact_enquiry_down(request):
    if request.method == "POST":
        mobile = request.POST['mobile_number']
        email_address = request.POST['email_address']
        try:
            enqp = request.POST['url_page_name']
        except:
            enqp = "Error to get page!!!"
        message = """Email Address: %s
Mobile Number: %s
Inquery Page : %s
For location Gurgaon""" %(email_address,str(mobile),enqp)
        print("Enquiry From Course -> contact_enquiry_down")
        print(message)
        if True:
            try:
                request.session['enquiry_sumited'] = True
                enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['bhart@goognu.com', 'ashutosh@ap2v.com', 'ravi@ap2vgurgaon.training'])
                enquiry_mail_obj.send()
                return redirect('thankyou')
            except Exception as e:
                print(e, "this is error")
                return JsonResponse({"result": e}, status=444)
        else:
            return JsonResponse({"result": False}, status=404)

#for send enquiry through mail for call
def contact_enquiry_call(request):
    if request.method == "POST":
        mobile = request.POST['mobile_number']
        try:
            enqp = request.POST['url_page_name']
        except:
            enqp = "Error to get page!!!"
        message = """Mobile Number: %s
Inquery Page : %s
For location Gurgaon""" %(str(mobile),enqp)
        print("Enquiry From Course -> contact_enquiry_down_call")
        print(message)
        if True:
            try:
                request.session['enquiry_sumited'] = True
                enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['bhart@goognu.com', 'ashutosh@ap2v.com', 'ravi@ap2vgurgaon.training'])
                enquiry_mail_obj.send()
                return redirect('thankyou')
            except Exception as e:
                print(e, "this is error")
                return JsonResponse({"result": e}, status=444)
        else:
            return JsonResponse({"result": False}, status=404)



#views for related course
def display_tag(request, tag, city_slug=False):
    print("8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
    # print(tag)
    # print(city_slug)
    context_data = {}
    courses = []
   
    if city_slug:
        filter_courses = City_Specific_Course.objects.filter(course__tags__slug__in=[tag],city__slug=city_slug)
        context_data['skill_course'] = filter_courses
        if filter_courses:
            for i in filter_courses:
                dict = {}
                dict['id']=i.id
                dict['slug']=i.slugs
                dict['course_icon']=i.course.course_icon
                dict['name']=i.name
                dict['category_name']=i.course.category_name
                dict['rating']=i.course.rating
                dict['review_count']=i.course.review_count
                dict['banner_text']=i.banner_text
                courses.append(dict)
    else:
        filter_courses = Courses.objects.filter(tags__slug__in=[tag],active_inactive=True)
        context_data['skill_course'] = filter_courses
        if filter_courses:
            for i in filter_courses:
                dict = {}
                dict['id']=i.id
                dict['slug']=i.slug
                dict['course_icon']=i.course_icon
                dict['name']=i.name
                dict['category_name']=i.category_name
                dict['rating']=i.rating
                dict['review_count']=i.review_count
                dict['banner_text']=i.banner_text
                courses.append(dict)
    
    filter_courses = City_Specific_Course.objects.filter(course__tags__slug__in=[tag],active_inactive=True,)
    print(filter_courses)
    temp_list = []
    city_block = []
    for course in filter_courses:
        tmp_d = {}
        tmp_d['name'] = course.city.name
        tmp_d['href'] = tag+"-courses-in-"+course.city.slug
        print(tmp_d)
        if not str(course.city.name) in temp_list:
            city_block.append(tmp_d)
        temp_list.append(course.city.name)
        print(temp_list)
    print(city_block)

    if len(filter_courses) < 1:
        raise Http404("Page does not exist.")
        #return redirect('/', permanent=True)
    else:
        category_queryset = Category.objects.all()[:8]
        context_data = {
                "courses": courses,"category_queryset":category_queryset,"city_block":city_block,'skill_course':filter_courses,'city__slug':city_slug
                }
        return render(request, 'v4_courses/course-listing.html', context_data)

class SearchFilterTemplateView(TemplateView):
    template_name = 'courses/search_filter.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchFilterTemplateView, self).get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        #context['search_datas'] = list(chain(
                                        #Courses.objects.all(),
                                        #Certifications.objects.all(),
                                        #CollegeCourses.objects.all()
                                    #))
        context['search_datas'] = SearchDataFilter(self.request.GET, queryset=Courses.objects.all()).qs
        return context

def check_enquiry(thankyou_function):
    def wrapper(tf_request):
        if tf_request.session.get("enquiry_sumited") != None or tr_request.session.get('refer_earn_sumited'):
            return thankyou_function(tf_request)
        return HttpResponseRedirect("/")
    return wrapper


@check_enquiry
def thankyou(request):
    context_data = {}
    return render(request, "home/thanks.html", context_data)

def trending_courses(request):
    ctx={}
    ctx['courses'] = Courses.objects.filter(trending=True,active_inactive=True).order_by('-price')

    return render(request, 'v4_courses/course-listing.html', ctx)

def featured_courses(request):
    ctx={}
    ctx['courses'] = Courses.objects.filter(featured=True,active_inactive=True).order_by('-price')

    return render(request, 'v4_courses/course-listing.html', ctx)


def load_course_content(request):
    ctx={}
    print("********************--------------------------------------------------1--------------------------------------------------********************************")

    slug= request.POST.get("slug",None)
    print(slug)
    if slug:
        if Courses.objects.filter(slug = slug,active_inactive=True).exists():
            courses_slug = Courses.objects.filter(slug=slug)
            if courses_slug.exists():
                ctx['lessons'] = Lessons.objects.filter(course=courses_slug.first()).order_by('index')[:6]

        elif City_Specific_Course.objects.filter(slugs = slug,active_inactive=True).exists():
            courses_slug = Courses.objects.filter(slug=slug)
            a = City_Specific_Course.objects.get(slugs=slug)
            courses_slug = a.course.slug

            ctx['lessons'] = Lessons.objects.filter(course=a.course.id).order_by('index')[:7]
    return render(request, 'v4_courses/course-content.html', ctx)


def load_course_content_full(request):
    ctx={}
    print("********************--------------------------------------------------2--------------------------------------------------********************************")

    slug= request.POST.get("slug",None)
    print(slug)
    if slug:
        if Courses.objects.filter(slug = slug,active_inactive=True).exists():
            courses_slug = Courses.objects.filter(slug=slug)
            if courses_slug.exists():
                ctx['lessons'] = Lessons.objects.filter(course=courses_slug.first()).order_by('index')

        elif City_Specific_Course.objects.filter(slugs = slug,active_inactive=True).exists():
            courses_slug = Courses.objects.filter(slug=slug)
            a = City_Specific_Course.objects.get(slugs=slug)
            courses_slug = a.course.slug

            ctx['lessons'] = Lessons.objects.filter(course=a.course.id).order_by('index')
    return render(request, 'v4_courses/course-content.html', ctx)

