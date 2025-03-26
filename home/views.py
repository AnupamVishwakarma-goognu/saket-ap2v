# from __future__ import unicode_literals
import time
from django.shortcuts import render,redirect
from blogs.models import Blogs ,Comments
from testimonials.models import Text, Video
from ap2v_courses.models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import SidebarCategory, Refer_and_Earn
from django.conf import settings
from home.models import Configrations
from events.models import *
from home.models import Location
from .models import Category, FeaturedCertifications
from django.core.mail import EmailMessage
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View, TemplateView
from django.http import Http404, HttpResponse
from itertools import chain
from learning_paths.models import Learning_Path
from recording_sessions.models import Recorded_Courses_name
# Create your views here.

live_configration_id = settings.LIVE_CONFIGRATION_ID
configration = Configrations.objects.filter(id=live_configration_id)
contact = Location.objects.all()
from enquiries.views import create_enquiry_api
from django.db.models import Q
from communication.models import CounselorContactNumber
from django.views.decorators.csrf import csrf_exempt
from batches.models import StudentCertificateIssued
from core.models import CountryCode

def home(request):
    home_display = True
    blogs = Blogs.objects.filter(show_on_site = True).order_by('-published_on')
    testimonials = Text.objects.order_by('-date')[:5]
    courses = Courses.objects.filter(active_inactive=True)
    events = Events.objects.order_by('-date')[:5]
    locations = Locations.objects.all()
    remote_items = RemoteItems.objects.all()
    all_city = City.objects.all()

    development_courses = {}
    linux_courses = {}
    database_courses = {}
    cloud_courses = {}
    bigdata_courses = {}

    category_obj = Category.objects.filter(slug='development')
    development_courses = Courses.objects.filter(category_name = category_obj.first(),active_inactive=True)
    category_linux = Category.objects.filter(slug='linux')
    linux_courses = Courses.objects.filter(category_name = category_linux.first(),active_inactive=True)
    database_obj = Category.objects.filter(slug='database')
    database_courses = Courses.objects.filter(category_name = database_obj.first(),active_inactive=True)
    cloud_obj = Category.objects.filter(slug='cloud')
    cloud_courses = Courses.objects.filter(category_name = cloud_obj.first(),active_inactive=True)
    bigdata_obj = Category.objects.filter(slug='bigdata')
    bigdata_courses = Courses.objects.filter(category_name = bigdata_obj.first(),active_inactive=True)
    learning_path_queryset = Learning_Path.objects.all().order_by('id')
    courses_on_header = Courses.objects.filter(banner_display = True,active_inactive=True)[:4]
    learning_path_header = Learning_Path.objects.filter(banner_display = True)[:4]
    certificate_queryset = FeaturedCertifications.objects.all()
    # category_all = Category.objects.all()
    # tranding_course_footer = Courses.objects.filter(trending = True)
    # listing_path_footer = Learning_Path.objects.filter(trending = True)

    category_home = Category.objects.filter(display_home=True).order_by('index')[:5]

    con_code_obj = CountryCode.objects.all()
    recording_courses = Recorded_Courses_name.objects.all()

    return render(request, 'v4_home/index.html',{'development_courses': development_courses,'linux_courses':linux_courses,
                            'database_courses':database_courses,'cloud_courses':cloud_courses,'bigdata_courses':bigdata_courses,
                            'blogs':blogs, 'testimonials':testimonials,'courses':courses,'events':events,
                            "locations": locations, 'remote_items': remote_items,'learning_path_queryset':learning_path_queryset,
                            'courses_on_header':courses_on_header,'category_home':category_home,
                            'certificate_queryset':certificate_queryset, 'home_display':home_display,'category_home':category_home,
                            'all_city':all_city,'con_code_obj':con_code_obj,'learning_path_header':learning_path_header,'recording_courses':recording_courses})


def send_enquiry(request):
    if request.method == "POST":
        try:
            enqp = request.POST['url_page_name']
        except:
            enqp = 'Error to get page!!!'

        try:
            name = request.POST['name']
        except:
            name = "N/A"

        mobile = request.POST['mobile_number']
        email_address = request.POST['email_address']

        try:
            text_message = "Request for demo of "+request.POST['course']
        except:
            text_message = request.POST['text_message']

        message = """        Enquiry Page Source : %s
        Name: %s
        Email Address: %s
        Mobile Number: %s
        Message: %s
        From ap2v.com""" % (enqp,name,email_address,str(mobile),text_message)
        print(message)
        if "http:" in text_message or "https:" in text_message:
            print("____________Contain LINK_____________________")
            return JsonResponse({"result": e}, status=444)
        else:
            print("____________NOT Contain LINK_____________________")
            try:
                # request.session['enquiry_sumited'] = True
                # enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
                # enquiry_mail_obj.send()
                # return thankyou(request)
                return redirect('thankyou')
                # return JsonResponse({"result": True}, status=200)
            except Exception as e:
                return JsonResponse({"result": e}, status=444)




# ----------------------------------------------------------------------------------------------------------------------------------------



# def home(request):
# 	blogs = Blogs.objects.order_by('-published_on')[:4]
# 	testimonials = Text.objects.order_by('-date')[:5]
# 	courses = Courses.objects.all()
# 	events = Events.objects.order_by('-date')[:5]
# 	certifications = Certifications.objects.all()
# 	locations = Locations.objects.all()
# 	remote_items = RemoteItems.objects.all()

# 	return render(request, 'home/home.html', {'blogs':blogs, 'testimonials':testimonials,'courses':courses,'events':events,'certifications':certifications, "locations": locations, 'remote_items': remote_items})

def about_us(request):
    clients = ['accenture.png', 'authbridge.png', 'collegedekho.png', 'ericsson.png', 'hcl.png', 'ht-media.png', 'ibm.png', 'india-air-force.png', 'innerchef.png', 'knowlarity.png', 'mercury-solutions.png', 'national-university-of-singapore.png', 'nokia.png', 'orange.png', 'paytm.png', 'redhat-academy.png', 'shine.png', 'tata-consultancy-services.png', 'tentaran.jpg', 'university-of-queensland.png', 'upkonnect.png']
    return render(request, 'home/about_us.html', {'clients': clients})

def contact_us(request):
	#return render(request, 'home/contact_us.html', {'header_text': configration.contect_us_header_text, "contact": contact})
    ctx = {}
    all_number = CounselorContactNumber.objects.all()
    ctx['all_number']=all_number
    return render(request, 'home/contact_us.html', ctx)

def offers(request):
	return render(request, 'home/offers.html', {})

def add_enquiry(request):
    if request.method == "POST":
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
        except:
            firstname = request.POST['name']
            lastname = ""
        mobile = request.POST['mobile_number']
        email_address = request.POST['email_address']
        try:
            text_message = "Request for demo of "+request.POST['course']
        except:
            text_message = request.POST['text_message']
        message = """Name: %s
Lastname: %s
Email Address: %s
for value in variable}for value in variable}Mobile Number: %s
Message: %s
From ap2v.com""" % (firstname,lastname,email_address,str(mobile),text_message)
        try:
            request.session['enquiry_sumited'] = True
            enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
            enquiry_mail_obj.send()
            return thankyou(request)
            # return JsonResponse({"result": True}, status=200)
        except Exception as e:
            return JsonResponse({"result": e}, status=444)

#def handler404(request, exception, template_name="home/404.html"):
#    response = render_to_response(template_name)
#    response.status_code = 404
#    return response

#def handler500(request, template_name="home/500.html"):
#    response = render_to_response(template_name)
#    response.status_code = 500
#    return response

def handler404(request):
    response = render(request, "home/404.html", {})
    response.status_code = 404
    return response

def handler500(request):
    response = render(request, "home/500.html", {})
    response.status_code = 500
    return response

def contact_enquiry(request):
    if request.method == "POST":
        try:
            enqp = request.POST['url_page_name']
        except:
            enqp = "Error to get page!!!"
        firstname = request.POST['firstname']
        mobile = request.POST['mobile_number']
        email_address = request.POST['email_address']
        text_message = request.POST['text_message']
        #captcha_code = request.POST['captcha_code']
        message = """Name: %s
Email Address: %s
Mobile Number: %s
Message: %s
Inquery Page : %s
For location Gurgaon""" %(firstname,email_address,str(mobile),text_message,enqp)
        print("Enquiry From Home -> contact_enquiry")
        print(message)
        if "http:" not in text_message and "https:" not in text_message:
            if True:
                try:
                    request.session['enquiry_sumited'] = True
                    enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
                    enquiry_mail_obj.send()
                    return JsonResponse({"result": request.POST}, status=200)
                except Exception as e:
                    print(e, "this is error")
                    return JsonResponse({"result": e}, status=444)
            else:
                    return JsonResponse({"result": False}, status=404)
        else:
            print("CONTANIN LINK")
            return JsonResponse({"result": False}, status=404)

def call_enquiry(request):
	if request.method == "POST":
		mobile = request.POST['mobile_number']
		email_address = request.POST['email_address']
		text_message = request.POST['text_message']
		try:
			enqp = request.POST['url_page_name']
		except:
			enqp = "Error to get page!!!"
		message = """Email Address: %s
Mobile Number: %s
Message: %s
Inquery Page : %s
For location Gurgaon""" %(email_address,str(mobile),text_message,enqp)
		print("Enquiry From Home -> call_enquiry")
		print(message)
		if True:
			try:
				request.session['enquiry_sumited'] = True
				enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
				enquiry_mail_obj.send()
				return JsonResponse({"result": request.POST}, status=200)
			except Exception as e:
				return JsonResponse({"result": e}, status=444)
		else:
			return JsonResponse({"result": False}, status=404)

def check_enquiry(thankyou_function):
    def wrapper(tf_request):
        if tf_request.session.get("enquiry_sumited") != None or tr_request.session.get('refer_earn_sumited'):
            return thankyou_function(tf_request)
        return HttpResponseRedirect("/")
    return wrapper


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
        print("Enquiry From Home -> contact_enquiry_down")
        print(message)
        if True:
            try:
                request.session['enquiry_sumited'] = True
                enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
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
		print("Enquiry From Home -> contact_enquiry_call")
		print(message)
		if True:
			try:
				request.session['enquiry_sumited'] = True
				enquiry_mail_obj = EmailMessage('Enquiry {enquiry_time}'.format(enquiry_time=str(time.ctime())), message, settings.EMAIL_HOST_USER, ['inquiry@ap2v.com'])
				enquiry_mail_obj.send()
				return redirect('thankyou')
			except Exception as e:
				print(e, "this is error")
				return JsonResponse({"result": e}, status=444)
		else:
			return JsonResponse({"result": False}, status=404)



def refer_and_earn(request):
    context_data = {}
    return render(request, 'home/refer-earn.html', context_data)

def refer_earn_register(request):
    context_data = {}
    if request.method == "POST":
        c_name = request.POST['c_name']
        c_phone = request.POST['c_phone']
        c_exists = request.POST['optionsRadios']
        if c_exists == 'yes':
            c_exists = True
        else:
            c_exists = False
        f_name = request.POST['f_name']
        f_phone = request.POST['f_phone']
        f_email = request.POST['f_email']
        f_designation = request.POST['f_designation']
        Refer_and_Earn.objects.create(candidate_name=c_name, candidate_phone=c_phone, candidate_exists=c_exists, friend_name=f_name, friend_phone=f_phone, friend_email=f_email, friend_designation=f_designation)
        request.session['refer_earn_sumited'] = True
        return JsonResponse({'result': True}, status=200)

def whyap2v(request):
    context_data = {}
    return render(request, 'home/100-reasons.html', context_data)

# @check_enquiry
def thankyou(request):
    context_data = {}
    return render(request, "home/thanks.html", context_data)

class PopUPSessionView(View):
    def get(self, *args, **kwargs):
        self.request.session['popup_value'] = True
        self.request.session.set_expiry(260)
        return JsonResponse({'result': True}, status=200)



def privacy_policy(request):
    
    return render(request,'v4_home/privacy_policy.html')

def terms_and_conditions(request):
    return render(request,'v4_home/term_and_condition.html')

def city_sitemap(request):
    ctx={}
    all_city = City.objects.all()
    ctx['all_city'] = all_city
    return render(request,'v4_home/city-sitemap.html',ctx)

def city_sitemap_category(request,city):
    ctx={}
    all_city = City.objects.all()
    ctx['all_city'] = all_city

    print(city)
    all_category = Category.objects.all()
    ctx['all_category'] = all_category
    ctx['city']=city

    return render(request,'v4_home/city-sitemap-category.html',ctx)

def sitemap(request):
    ctx={}
    all_category = Category.objects.all()
    ctx['all_category'] = all_category
    return render(request,'v4_home/sitemap.html',ctx)

def error_4xx(request,exception=None):
    return render(request,'v4_home/error_4xx.html', status=404)

def error_5xx(request):
    return render(request,'v4_home/error_5xx.html')

# -----function for save add_enquiry----------
def create_enquiry(request):
    if not request.POST._mutable:
        request.POST._mutable = True
        request.POST['key'] = "CONNTOANQUIRA@3685"
    a = create_enquiry_api(request)
    if a.status_code == 200:
        return JsonResponse({"code": 1})
    else:
        return JsonResponse({"code": 0})
# ------- End Function --------------------------

@csrf_exempt
def find(request):
    ctx={}
    string = request.POST.get('string',None)
    # print(string)
    if string:
        # print(string)
        course_obj = Courses.objects.filter(Q(name__icontains=string) | Q(description__icontains=string),active_inactive=True)
        ctx['course_obj']=course_obj
        # print(ctx['course_obj'])
    return render(request,'v4_home/sub_pages/search_result.html',ctx)

def search(request):
    ctx={}
    string = request.GET.get('string',None)
    print(string)
    if string:
        # print(string)
        course_obj = Courses.objects.filter(Q(name__icontains=string) | Q(description__icontains=string),active_inactive=True)
        ctx['courses']=course_obj

        category_queryset = Category.objects.all()[:8]
        ctx['category_queryset'] = category_queryset

        return render(request, 'v4_courses/course-listing.html', ctx)
    return render(request,'v4_home/sub_pages/search_result.html',ctx)

def verify(request):
    ctx={'seo': {}}
    ctx['seo']['title'] = 'Verify Your Certificate - AP2V Academy'
    certId = request.GET.get("certId",None)
    name_certi_obj = StudentCertificateIssued.objects.filter(code=certId).first()
    if name_certi_obj:
        student_name = name_certi_obj.enroll.enquiry_course_id.enquiry_id.full_name
        ctx['student_name']=student_name
    if certId:
        certificate_obj = StudentCertificateIssued.objects.filter(code=certId)
        ctx['certificate_obj']=certificate_obj
        ctx['certId']=certId
    return render(request,'v4_home/certificate_verify.html',ctx)