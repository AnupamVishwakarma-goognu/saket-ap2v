from pickle import NONE
from unicodedata import name
from django.shortcuts import redirect, render
from bluejeans.zoom import get_user_details,get_user_details_test,zoom_scheduled_meeting,zoom_scheduled_meeting_test,assign_license_to_user_test,inc_meeting_license_number,dec_meeting_license_number
from ap2v_courses.models import Courses
from learning_paths.models import Learning_Path
from home.models import Category
import datetime
from users.models import CustomUserModel as User
# from users.customcode import authenticate
from django.contrib.auth import login as auth_login,authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from enrolls.models import Enrollments
from batches.models import Batches,StudentCertificateIssued,ZoomLicenseDetails,ZoomMeetingIdUserBatch
import requests
import json
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings,get_recordings_url_by_composite_id
import random
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import calendar
from demo.models import Demo,DemoSaveVideo
from enquiries.models import Enquiries,EnquiryCourses

import urllib
import requests
import shutil
from django.conf import settings
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
import os
import datetime
import re
from collections import OrderedDict
from classroom.models import BatchStudentFeedback
from users.views import genrate_verification_token

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from bluejeans.views import scheduled_meeting,genrate_bitly_link
from recording_sessions.models import Recorded_Courses_name
# from .models import OfferCourse
from .models import ClassRoomCourseOffer,StudyMaterial
# Create your views here.

@csrf_exempt
def get_study_materials(request):
    if request.method == "POST":
        print("POST R<ASNM<DF M")
        batch_id = request.POST.get('batch_id')
        data=""
        # print("BATCH ID:",batch_id)

        if batch_id:
            study_materials = StudyMaterial.objects.filter(batch_id=batch_id)
            # study_materials = StudyMaterial.objects.all()
            data = [{'name': os.path.basename(material.file.name), 'url': material.file.url} for material in study_materials]
            return JsonResponse(data, safe=False)
        else:
            return None
    else:
        return None

@csrf_exempt
@login_required(login_url='/')
def classroom(request):
    ctx={'seo': {}}

    ctx['tab_classroom'] = "active"
    ctx['classroom'] = "true"
    ctx['seo']['title'] = 'Classroom - AP2V Academy'

    ctx['tranding_course_footer']=Courses.objects.filter(trending = True,active_inactive=True)
    ctx['listing_path_footer']=Learning_Path.objects.filter(trending = True)
    ctx['category_all']=Category.objects.all()
    if request.user.user_type == "student":
        # enroll_data = Enrollments.objects.filter(enquiry_course_id__enquiry_id__email = request.user.email)
        enroll_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email)
        # enroll_data = Enrollments.objects.filter(enquiry_course_id__enquiry_id__email = request.user.email).values_list('batch', flat=True)
        ctx['enroll_data']=enroll_data

        stu_certificate_obj = StudentCertificateIssued.objects.filter(user = request.user.id)
        ctx['stu_certificate_obj']=stu_certificate_obj

        ''' Find the Offer course for showing in 
            classroom with discount in banner
        '''
        enrolls_data = list(Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email).values_list("courses",flat=True))
        enroll_course_course_obj = list(Courses.objects.filter(anquira_course_id__in = enrolls_data).values_list("id", flat=True))
        offer_course_obj = ClassRoomCourseOffer.objects.filter(relevant_course__in = enroll_course_course_obj).exclude(course__in = enroll_course_course_obj)

        final_offer_course_dict = []
        for i in offer_course_obj:
            temp_dict = {}
            today_date = datetime.datetime.now().date() 
            if i.discount_valid_till >= today_date:
                price = i.course.anquira_course.price
                discount_price =int(price*(100-i.discount)/100)

                temp_dict['id'] = i.course.id
                temp_dict['orignal_price'] = i.course.anquira_course.original_price
                temp_dict['price'] = discount_price
                temp_dict['name'] = i.course.name
                temp_dict['image'] = i.course.course_icon
                temp_dict['offer_date'] = i.discount_valid_till

            else:
                price = i.course.anquira_course.price
                discount_price =int(price*(100-i.discount_after_date)/100)

                temp_dict['id'] = i.course.id
                temp_dict['orignal_price'] = i.course.anquira_course.original_price
                temp_dict['price'] = discount_price
                temp_dict['name'] = i.course.name
                temp_dict['image'] = i.course.course_icon
            final_offer_course_dict.append(temp_dict)
        ctx['offers']=final_offer_course_dict
        '''End offer code
        '''

    elif request.user.user_type == "instructor":
        filter_batch_type = request.GET.get("batch_filter",None)
        ctx['filter_batch_type']=filter_batch_type
        if filter_batch_type=="batch-completed":
            ctx['seo']['title'] = 'Classroom :: Completed batches - AP2V Academy'
            all_instructor_batch = Batches.objects.filter(Q(instructors__email = request.user.email,end_date_time__lte = datetime.datetime.today().date()) | Q(batch_status__in = [1,2,3,5])).order_by("-id")
            all_instructor_batch = all_instructor_batch.filter(instructors__email = request.user.email)
            ctx['batch_status'] = "batch-completed"
        else:
            all_instructor_batch = Batches.objects.filter(instructors__email = request.user.email,end_date_time__gte = datetime.datetime.today().date()).order_by("-id")
            all_instructor_batch = all_instructor_batch.filter(batch_status = 4)
            ctx['batch_status'] = "batch-run"
        ctx['all_instructor_batch']=all_instructor_batch
    
    return render(request,'classroom/classroom.html',ctx)

def course_materials(request,active_link=None):
    ctx={}
    
    ctx['tab_course_material'] = "active"
    ctx['active_link'] = active_link
    ctx['tranding_course_footer']=Courses.objects.filter(trending = True,active_inactive=True)
    ctx['listing_path_footer']=Learning_Path.objects.filter(trending = True)
    ctx['category_all']=Category.objects.all()
    if request.user.user_type == "student":
        enroll_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email)
        ctx['enroll_data']=enroll_data
    elif request.user.user_type == "instructor":
        all_instructor_batch = Batches.objects.filter(instructors__email = request.user.email,complete=False).order_by("-id")
        ctx['all_instructor_batch']=all_instructor_batch
    return render(request,'classroom/course_materials.html',ctx)

def curriculum(request,active_link=None):
    ctx={'seo': {}}
    ctx['seo']['title'] = 'Classroom :: Course curriculum - AP2V Academy'
    ctx['tab_course_curriculum'] = "active"
    ctx['active_link'] = active_link

    filter_batch_type = request.GET.get("batch_filter",None)
    ctx['batch_status'] = filter_batch_type

    batch = active_link[7:]
    batch_data = Batches.objects.filter(batch_name=batch).first()
    ctx['batch_data'] = batch_data
    ctx['tranding_course_footer']=Courses.objects.filter(trending = True,active_inactive=True)
    ctx['listing_path_footer']=Learning_Path.objects.filter(trending = True)
    ctx['category_all']=Category.objects.all()
    if request.user.user_type == "student":
        enroll_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email)
        ctx['enroll_data']=enroll_data
    elif request.user.user_type == "instructor":
        if filter_batch_type=="batch-completed":
            all_instructor_batch = Batches.objects.filter(instructors__email = request.user.email,end_date_time__lte = datetime.datetime.today().date()).order_by("-id")
        else:
            all_instructor_batch = Batches.objects.filter(instructors__email = request.user.email,end_date_time__gte = datetime.datetime.today().date()).order_by("-id")

        ctx['all_instructor_batch']=all_instructor_batch
    return render(request,'classroom/curriculum.html',ctx)

def feedback(request,active_link=None):
    ctx={'seo': {}}
    ctx['seo']['title'] = 'Classroom :: Feedback - AP2V Academy'
    ctx['tab_feedback'] = "active"
    ctx['active_link'] = active_link
    ctx['tranding_course_footer']=Courses.objects.filter(trending = True,active_inactive=True)
    ctx['listing_path_footer']=Learning_Path.objects.filter(trending = True)
    ctx['category_all']=Category.objects.all()
    if request.user.user_type == "student":
        enroll_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email)
        ctx['enroll_data']=enroll_data
    elif request.user.user_type == "instructor":
        all_instructor_batch = Batches.objects.filter(instructors__email = request.user.email,complete=False).order_by("-id")
        ctx['all_instructor_batch']=all_instructor_batch
    return render(request,'classroom/feedback.html',ctx)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username =  request.POST['email']
            password = request.POST['password']
            check_login = authenticate(username=username, password = password)
            if check_login is not None:
                if check_login.user_type =="student" or check_login.user_type =="instructor":
                    auth_login(request, check_login)
                    return redirect('classroom')
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
@csrf_exempt
def attemptuserLogin(request):
    data={}
    if request.user.is_authenticated:
        data['status']=200
    else:
        if request.method == "POST":
            username =  request.POST.get('email',None)
            password = request.POST.get('password',None)
            check_login = authenticate(username=username, password = password)
            if check_login is not None:

                if check_login.user_type =="student" or check_login.user_type =="instructor":
                    if check_login.is_verified == False:
                        genrate_verification_token(request,check_login.first_name,check_login.email,password="abc")
                        data['message']="We have send a verification Email, Please verify your Email."
                        data['status']=400
                    else:
                        auth_login(request, check_login)
                        data['status']=200
                else:
                    data['message']="Something is wrong, Please try again"
                    data['status']=400
            else:
                data['message']="Username and Password incorrect."
                data['status']=400
    return JsonResponse(data)

def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return redirect('/')



def system_requirements(request):
    return render(request,'classroom/system_requirements.html')

def signup(request):
    name = request.POST.get("fullname",None)
    email = request.POST.get("email",None)
    password = request.POST.get("password",None)

    x = User(
        first_name = name,
        email = email.lower(),
        username = email,
        user_type = 'student',
    )
    x.set_password(password)
    x.save()
    return redirect('/')

@csrf_exempt
def get_recording(request):
    ctx={}
    import datetime
    bid = request.POST.get("meeting_id",None)
    batch_obj = Batches.objects.filter(id = bid).first()
    ACCESS_KEY = settings.ACCESS_KEY
    SECRET_KEY = settings.AWS_SECRET_KEY
    BUCKETNAME = settings.BUCKETNAME

    bucket = BUCKETNAME
    folder = "batch"+str("/")+str(batch_obj.id)+str("/")
    sesssion  = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    s3 = sesssion.resource('s3')
    bucketName = BUCKETNAME
    bucket = s3.Bucket(bucketName)

    batch_classes = []
    for obj in bucket.objects.filter(Prefix=folder):
        batch_classes.append(obj.key)
    
    
    recording = []
    l = batch_classes
    l_dict = {}

    total_length = 0
    
    for f in l:
        # re_obj = re.search(".*_((\d{8})\d{6})_.*", f)
        re_obj = re.search(r".*_((\d{8})\d{6})_.*", f)
        if re_obj:
            recorded_on = re_obj.group(1)
            l_dict[recorded_on] = f
        
        split_batch_classes = (((f.split("_"))[-1]).split("."))[0]
        try:
            total_length = total_length + int(split_batch_classes)
        except Exception as e:
            print(e)
    sorted_by_date = [l_dict[r] for r in sorted(l_dict.keys())]

    split_by_date = OrderedDict()
    for r in sorted_by_date:
        # re_obj = re.search(".*_((\d{8})\d{6})_.*", r)
        re_obj = re.search(r".*_((\d{8})\d{6})_.*", r)
        if re_obj:
            recorded_on = re_obj.group(2)
            if  recorded_on in split_by_date:
                split_by_date[recorded_on].append(r)
            else:
                split_by_date[recorded_on] = []
                split_by_date[recorded_on].append(r)


    ctx['recording']=split_by_date
    batch_obj = Batches.objects.filter(id=bid).last()
    ctx['batch_obj']=batch_obj
    ctx['recording_count']=len(batch_classes)
    ctx['total_minute'] =total_length
    return render(request,'classroom/classroom_recordings.html',ctx)

# aashish fun get_recording_left
@csrf_exempt
def get_recording_left_side(request):
    ctx={}
    import datetime
    bid = request.POST.get("meeting_id",None)
    url = request.POST.get("url",None)
    url = url.split("@")[2]
    url = url.split("_")[0]
    ctx['url']=url

    if bid:
        batch_obj = Batches.objects.filter(id = bid).first()

        ACCESS_KEY = settings.ACCESS_KEY
        SECRET_KEY = settings.AWS_SECRET_KEY
        BUCKETNAME = settings.BUCKETNAME

        bucket = BUCKETNAME
        folder = "batch"+str("/")+str(batch_obj.id)+str("/")
        sesssion  = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        s3 = sesssion.resource('s3')
        bucketName = BUCKETNAME
        bucket = s3.Bucket(bucketName)

        batch_classes = []
        for obj in bucket.objects.filter(Prefix=folder):
            batch_classes.append(obj.key)
        
        
        recording = []
        l = batch_classes
        l_dict = {}

        total_length = 0
        
        for f in l:
            # re_obj = re.search(".*_((\d{8})\d{6})_.*", f)
            re_obj = re.search(r".*_((\d{8})\d{6})_.*", f)
            if re_obj:
                recorded_on = re_obj.group(1)
                l_dict[recorded_on] = f
            
            try:
                total_length = total_length + int(split_batch_classes)
            except Exception as e:
                print(e)
        sorted_by_date = [l_dict[r] for r in sorted(l_dict.keys())]

        split_by_date = OrderedDict()

        for r in sorted_by_date:
            # re_obj = re.search(".*_((\d{8})\d{6})_.*", r)
            re_obj = re.search(r".*_((\d{8})\d{6})_.*", r)
            if re_obj:
                recorded_on = re_obj.group(2)
                if  recorded_on in split_by_date:
                    split_by_date[recorded_on].append(r)
                else:
                    split_by_date[recorded_on] = []
                    split_by_date[recorded_on].append(r)

        ctx['recording']=split_by_date
        batch_obj = Batches.objects.filter(id=bid).last()
        ctx['batch_obj']=batch_obj
        ctx['recording_count']=len(batch_classes)
        ctx['total_minute'] =total_length

    return render(request,'classroom/recording_play_list.html',ctx)

@login_required(login_url='/')
def download_certificate(request,batch_name,slug):
    ctx={}
    batch_obj = Batches.objects.filter(chat_room_id=slug).last()
    if batch_obj:
        if batch_obj.batch_name == batch_name:
            course_list = []
            for j in batch_obj.courses.all():
                course_list.append(j.name)

            c_name = " and ".join(course_list)

            ctx['student_name'] = request.user.first_name
            ctx['course_name'] = c_name
            ctx['certificate_code'] = str(batch_obj.batch_name)[6:]
            ctx['complete_date'] = batch_obj.end_date_time
    return render(request,'classroom/certificate.html',ctx)

def recording_play(request, composite_id, user):
    ctx={}
    url = get_recordings_url_by_composite_id(request,composite_id,user)
    ctx['url'] = url
    return render(request,'classroom/recording_play.html',ctx)

@login_required(login_url='/')
def class_recording_play(request, class_link):
    ctx={}
    batch_id = (class_link.split("@"))[1]
    batch_mi = (class_link.split("@"))[2]
    ctx['batch_id']=batch_id
    ctx['batch_mi']=batch_mi
    sp=batch_mi.split('_')[0]
    ctx['meeting']=sp
    '''Geting batch details'''
    batch_obj = Batches.objects.filter(id=batch_id).first()
    if batch_obj:
        ctx['batch_id'] = batch_obj.id
        course_list = []
        batch_course_obj = batch_obj.courses.all()
        for coi in batch_course_obj:
            course_list.append(coi.name)
        # print("*"*50)
        # print(course_list)
        ctx['batch_name'] = " and ".join(course_list)
        enroll_student_email_list = []
        for i in batch_obj.enroll_student.all():
            student_email = i.enquiry_course_id.enquiry_id.email
            if student_email:
                enroll_student_email_list.append(student_email)
    login_user_email = request.user.email
    enroll_student_email_list.append(batch_obj.instructors.email)
    enroll_student_email_list.append('neeraj@goognu.com')
    enroll_student_email_list.append('neerajkumar1248.nk@gmail.com')
    enroll_student_email_list.append('testplay@ap2v.com')
    if login_user_email in enroll_student_email_list:
        
        url = ''
        class_link = class_link.replace("@",'/')


        ACCESS_KEY = settings.ACCESS_KEY
        SECRET_KEY = settings.AWS_SECRET_KEY
        BUCKETNAME = settings.BUCKETNAME

        expiration=3600
        bucket_name = BUCKETNAME
        object_name = class_link

        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        try:
            response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
            url = response
        except Exception as e:
            print(e)
        
        ctx['url'] = url
        certificate_obj = StudentCertificateIssued.objects.filter(batch=batch_obj.id,user=request.user.id).last()
        if certificate_obj:
            ctx['certificate_obj'] = certificate_obj
        return render(request,'classroom/recording_play.html',ctx)
    else:
        ctx['play_error'] = "you are not authorized to view this page."
        return render(request,'v4_home/error_course_not_found.html', ctx, status=404)

def class_recording_demo_play(request, class_link):
    ctx={}
    url = ''
    class_link = class_link.replace("@",'/')

    ACCESS_KEY = settings.ACCESS_KEY
    SECRET_KEY = settings.AWS_SECRET_KEY
    BUCKETNAME = settings.BUCKETNAME

    expiration=3600
    bucket_name = BUCKETNAME
    object_name = class_link

    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
        url = response
    except Exception as e:
        print(e)
    
    ctx['url'] = url
    return render(request,'classroom/recording_play.html',ctx)

@csrf_exempt
def get_batch_student_details(request):
    ctx = {}
    batch_id = request.POST.get("batch_id",None)
    if batch_id:
        batch_obj = Batches.objects.filter(id=batch_id).first()
        all_batch_student = batch_obj.enroll_student.all()
        # print(batch_obj.enroll_student.all().count())
        all_student_list = []
        for i in all_batch_student:
            student_dict = {}
            student_dict['name'] = i.enquiry_course_id.enquiry_id.full_name
            student_dict['email'] = i.enquiry_course_id.enquiry_id.email
            student_dict['mobile'] = i.enquiry_course_id.enquiry_id.mobile
            student_dict['dropped'] = i.dropped
            student_dict['id'] = i.id

            all_student_list.append(student_dict)
    ctx['all_student_list']=all_student_list
    return render(request,'classroom/batch_student_details.html',ctx)


def weeknum(dayname):
	if dayname == 'Monday':   return 0
	if dayname == 'Tuesday':  return 1
	if dayname == 'Wednesday':return 2
	if dayname == 'Thursday': return 3
	if dayname == 'Friday':   return 4
	if dayname == 'Saturday': return 5
	if dayname == 'Sunday':   return 6



@csrf_exempt
def calender(request):
    from datetime import timedelta
    ctx={}
    all_batch_obj = Batches.objects.filter(instructors__email = request.user.email,complete=False,batch_status=4).order_by("-id")
    all_date = []
    today_date = []

    for i in all_batch_obj:
        batch_start_date = i.start_date_time.date()
        batch_end_date = i.end_date_time.date()

        start_time = i.start_date_time.time()

        course_list = []
        for j in i.courses.all():
            course_list.append(j.name)

        days = i.days_of_week.split(",")
        for day in days:
            whichDayYouWant = day
            days_date = [batch_start_date + timedelta(days=x) for x in range((batch_end_date-batch_start_date).days + 1) if (batch_start_date + timedelta(days=x)).weekday() == weeknum(whichDayYouWant)]
            for d in days_date:
                batch_date_dict = {}
                batch_date_dict['title'] = " and ".join(course_list)
                batch_date_dict['start'] = datetime.datetime.combine(d,start_time)
                batch_date_dict['color'] = ''
                batch_date_dict['url'] = str(i.id)+str("*batch")
                all_date.append(batch_date_dict)
                
                if d == datetime.date.today():
                    today_batch_date = {}
                    today_batch_date['title'] = " and ".join(course_list)
                    today_batch_date['start'] = datetime.datetime.combine(d,start_time)
                    today_batch_date['url'] = i.bitly_link_instructer
                    today_date.append(today_batch_date)


    demo_obj = Demo.objects.filter(instructors__email = request.user.email,start_date_time__gte=datetime.date(2021, 9, 4))
    for demo in demo_obj:
        demo_dict = {}
        demo_dict['title']="Demo for "+ demo.courses.name
        demo_dict['start']=demo.start_date_time
        demo_dict['color']='#378006'
        demo_dict['url'] = str(demo.id)+str("*demo")
        all_date.append(demo_dict)

        if demo.start_date_time.date() == datetime.date.today():
            today_demo_batch_date = {}
            today_demo_batch_date['title'] = "Demo for "+ demo.courses.name
            today_demo_batch_date['start'] = demo.start_date_time
            today_demo_batch_date['url'] = demo.bitly_link_instructer
            today_date.append(today_demo_batch_date)

    ctx['all_date']=all_date
    ctx['today_date']=today_date
    ctx['today']=datetime.date.today()
    return render(request,'classroom/calender.html',ctx)

@csrf_exempt
def get_calender_day_event(request):
    data = {}
    id_and_type = request.POST.get('id_type',None)
    id_and_type = id_and_type.split("*")
    if id_and_type[1] == "batch":
        id = id_and_type[0]
        
        batch_obj = Batches.objects.filter(id = id).first()

        course_list = []
        for j in batch_obj.courses.all():
            course_list.append(j.name)

        data['name'] = " and ".join(course_list)
        dt = (batch_obj.start_date_time+ datetime.timedelta(hours=5,minutes=30)).time()
        data['time'] = dt.strftime("%I:%M %p")
        data['url'] = batch_obj.bitly_link_instructer
    elif id_and_type[1] == "demo":
        id = id_and_type[0]
        batch_obj = Demo.objects.filter(id = id).first()
        data['name'] = "Demo for "+ batch_obj.courses.name
        dt = (batch_obj.start_date_time+ datetime.timedelta(hours=5,minutes=30)).time()
        data['time'] = dt.strftime("%I:%M %p")
        data['url'] = batch_obj.bitly_link_instructer
    else:
        data['name'] = ""
        data['time'] = ""
        data['url'] = ""

    return JsonResponse(data)


def submitStudentFeeback(request):
    data={}
    batch_id = request.POST.get("batch_id",None)
    rating = request.POST.get("rating",None)
    comment = request.POST.get("comment",None)
    batch_id = batch_id[7:]
    batch_obj = Batches.objects.filter(batch_name=batch_id).first()

    if batch_obj:
        x = BatchStudentFeedback(
            user_id = request.user.id,
            batch_id = batch_obj.id,
            rating = rating,
            comment = comment
        )
        x.save()
    
    else:
        x = BatchStudentFeedback(
            user_id = request.user.id,
            rating = rating,
            comment = comment
        )
        x.save()
    
    
    subject = 'Feedback Received'
    message = 'Received one feedback from "{0}" on batch id "{1}" with rating "{2}" and comment is \n\n {3}'.format(request.user.name,str(batch_obj.id),rating,comment)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = settings.FEEDBACK_EMAIL_NOTIFICATION
    send_mail( subject, message, email_from, recipient_list )

    data['status']=200
    return JsonResponse(data)


def genrate_certificate(request,slug):
    ctx={}
    stu_cert_obj = StudentCertificateIssued.objects.filter(uuid = slug).last()
    if stu_cert_obj:
        ctx['student_name'] = stu_cert_obj.name
        ctx['course_name'] = stu_cert_obj.course
        ctx['certificate_code'] = stu_cert_obj.code
        ctx['complete_date'] = stu_cert_obj.date
        ctx['stu_data']=stu_cert_obj
    return render(request,'classroom/certificate.html',ctx)

def mark_stu_attendance(request):
    data={}
    batch_id = request.POST.get("batch_id",None)
    if batch_id:
        if request.user.is_authenticated:
            batch_obj = Batches.objects.filter(id=batch_id).first()
            student_attendance = batch_obj.student_attendance
            today_date = str(datetime.date.today())
            if student_attendance:
                json_acceptable_string = student_attendance.replace("'", "\"")
                student_attendance = json.loads(json_acceptable_string)

            if student_attendance:
                if today_date in student_attendance:
                    attendance_data = student_attendance[today_date]
                    login_user = request.user.id
                    attendance_data.append(login_user)
                    attendance_data = list(set(attendance_data))
                    student_attendance[today_date] = attendance_data
                    Batches.objects.filter(id=batch_id).update(
                        student_attendance = student_attendance
                    )
                else:
                    stu_list = []
                    login_user = request.user.id
                    stu_list.append(login_user)
                    student_attendance[today_date] = stu_list
                    Batches.objects.filter(id=batch_id).update(
                        student_attendance = student_attendance
                    )
            else:
                student_attendance = {}
                today_date = str(datetime.date.today())
                stu_list = []
                login_user = request.user.id
                stu_list.append(login_user)
                student_attendance[today_date] = stu_list
                Batches.objects.filter(id=batch_id).update(
                    student_attendance = student_attendance
                )

    return JsonResponse(data)

def get_batch_student_attendance_details(request):
    ctx={}
    batch_id = request.POST.get("batch_id",None)
    if batch_id:
        batch_obj = Batches.objects.filter(id=batch_id).first()
        student_attendance = batch_obj.student_attendance
        if student_attendance:
            json_acceptable_string = student_attendance.replace("'", "\"")
            student_attendance = json.loads(json_acceptable_string)
            ctx['student_attendance']=student_attendance
    return render(request,"classroom/batch_student_attendance.html",ctx)

def mark_joined(request):
    data={}
    batch_id = request.POST.get("batch_id",None)
    if batch_id:
        batch_obj = Batches.objects.filter(id=batch_id).update(
            last_join_datetime = datetime.datetime.now(),
            is_alert_send = False,
        )
    return JsonResponse(data)

def playback(request, class_link):
    ctx={}
    url = ''
    class_link = class_link.replace("@",'/')

    ACCESS_KEY = settings.ACCESS_KEY
    SECRET_KEY = settings.AWS_SECRET_KEY
    BUCKETNAME = settings.BUCKETNAME

    expiration=3600
    bucket_name = BUCKETNAME
    object_name = class_link

    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
        url = response
    except Exception as e:
        print(e)
    
    ctx['url'] = url
    return render(request,'classroom/recording_play.html',ctx)

def mark_batch_as_completed_by_instructor(request):
    data={}
    if request.method=="POST":
        batch_id = request.POST.get("batch_id",None)
        # print(batch_id)

        batch_obj = Batches.objects.filter(id=batch_id).first()
        # print(batch_obj.batch_status)
        if batch_obj:
            if batch_obj.batch_status == "5":
                # print("Number 5")
                Batches.objects.filter(id=batch_id).update(
                batch_status = 4
                )
                data['msg'] = "Batch Marked as running"
            elif batch_obj.batch_status == "4":
                # print("Number 4")
                Batches.objects.filter(id=batch_id).update(
                    batch_status = 5
                )
                data['msg'] = "Batch Marked as complete"
    else:
        data['msg'] = "Something went wrong... Try again."
    
    # print(data)
    return JsonResponse(data)

def start_batch(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
    if batch_id:
        ctx['batch_id'] = batch_id
    else:
        ctx['errpr']  = "Bath is not exists....."
    return render(request,'classroom/batch_waiting_page_student.html',ctx)

def getting_student_batch_details(request):
    ctx={}
    batch_id = request.POST.get("batch_id",None)
    meeting_responce = None

    batch_obj = Batches.objects.filter(id=batch_id).first()
    if batch_obj:
        zoom_bitly_link_student_mobile = batch_obj.zoom_bitly_link_student_mobile
        if zoom_bitly_link_student_mobile:
            ctx['code'] = 1
            ctx['stu_link'] = zoom_bitly_link_student_mobile
        else:
            ctx['code']=0
            ctx['error']="Meeting is not started by host."

    return JsonResponse(ctx)

def join_batch(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
    if batch_id:
        ctx['batch_id'] = batch_id
        batch_obj = Batches.objects.filter(id=batch_id).first()
        if batch_obj.zoom_bitly_link_instructer:
            ctx['inst_link'] = batch_obj.zoom_bitly_link_instructer
            ctx['old_mid'] = 1
    else:
        ctx['errpr']  = "Bath is not exists....."
    return render(request,'classroom/batch_waiting_page_inst.html',ctx)

def join_batch_test(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
    if batch_id:
        ctx['batch_id'] = batch_id
        batch_obj = Batches.objects.filter(id=batch_id).first()
        if batch_obj.zoom_bitly_link_instructer:
            ctx['inst_link'] = batch_obj.zoom_bitly_link_instructer
            ctx['old_mid'] = 1
    else:
        ctx['errpr']  = "Bath is not exists....."
    return render(request,'classroom/batch_waiting_page_inst_test.html',ctx)


def getting_meeting_details_test(request):
    ctx={}
    batch_id = request.POST.get("batch_id",None)
    meeting_responce = None

    batch_obj = Batches.objects.filter(id=batch_id).first()
    if batch_id:
        email = batch_obj.instructors.email
        status_code,response,token = get_user_details_test(email)
        if status_code == 200:
            user_type = response['type']
            if user_type == 2:
                course_list = []
                for j in batch_obj.courses.all():
                    course_list.append(j.name)
                batch_title = " & ".join(course_list) 
                
                nowDateTime = datetime.datetime.now()

                dec_meeting_license_number()

                batch_start_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                from datetime import timedelta
                batch_end_date_time = nowDateTime+timedelta(minutes=180)
                batch_end_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                meeting_responce,zoom_password_random = zoom_scheduled_meeting_test(request,title=batch_title,description=None,start=batch_start_date_time,end=batch_end_date_time,attendees_list=None,zoom_user_email = email,token=token)
            elif user_type == 1:
                license_obj = ZoomLicenseDetails.objects.all().last()
                total_license = license_obj.total_license
                use_license = license_obj.use_license
                free_license = int(total_license) - int(use_license)
                if free_license > 0:
                    responce = assign_license_to_user_test(email,token)
                    check_licence_response = get_user_details_test(email)
                    user_type = check_licence_response[1]['type']
                    if user_type == 2:
                        dec_meeting_license_number()
                        if responce == 204:
                            course_list = []
                            for j in batch_obj.courses.all():
                                course_list.append(j.name)
                            batch_title = " & ".join(course_list) 
                            
                            nowDateTime = datetime.datetime.now()

                            batch_start_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")

                            from datetime import timedelta
                            batch_end_date_time = nowDateTime+timedelta(minutes=180)
                            batch_end_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                            meeting_responce,zoom_password_random = zoom_scheduled_meeting_test(request,title=batch_title,description=None,start=batch_start_date_time,end=batch_end_date_time,attendees_list=None,zoom_user_email = email,token=token)
                        else:
                            ctx['code'] = 0
                            ctx['error'] = "Meeting is not creating because licence is not free at this time..."
                    else:
                        ctx['code'] = 0
                        ctx['error'] = "No free licence is available on zoom..."
                else:
                    ctx['code'] = 0
                    ctx['error'] = "Licence is not free at this time...."
            else:
                ctx['error'] = "Error With User on Zoom Site..."

            if meeting_responce:
                meeting_id = meeting_responce['id']
                zoom_inst_url = meeting_responce['start_url']
                zoom_stu_url = meeting_responce['join_url']
                instructor_meeting_link_bitly = zoom_inst_url
                student_meeting_link_bitly = zoom_stu_url
                Batches.objects.filter(id=batch_id).update(
                    zoom_meeting_id = meeting_id,
                    zoom_meeting_password = zoom_password_random,
                    zoom_bitly_link_instructer = instructor_meeting_link_bitly,
                    zoom_bitly_link_student_mobile = student_meeting_link_bitly,
                    zoom_response_logs = meeting_responce
                )


                x = ZoomMeetingIdUserBatch(
                    meeting_type = 1,
                    batch_id = batch_id,
                    meeting_id = meeting_id,
                    meeting_status = '1',
                    zoom_meeting_password = zoom_password_random,
                    zoom_bitly_link_instructer = instructor_meeting_link_bitly,
                    zoom_bitly_link_student_mobile = student_meeting_link_bitly,
                    zoom_response_logs = meeting_responce,
                    meeting_start_at = datetime.datetime.now(),
                )
                x.save()

                print("Meeting Log created....")

                ctx['code'] = 1
                ctx['success'] = "yes"
                ctx['inst_link'] = instructor_meeting_link_bitly
        else:
            ctx['code'] = 0
            ctx['error'] = "Error to get your details from zoom server or user may be not registered on zoom"
    else:
        ctx['code'] = 0
        ctx['error'] = "Batch id is invalid..."
    return JsonResponse(ctx)





def getting_meeting_details(request):
    ctx={}
    batch_id = request.POST.get("batch_id",None)
    meeting_responce = None
    print(batch_id)

    batch_obj = Batches.objects.filter(id=batch_id).first()
    if batch_id:
        email = batch_obj.instructors.email
        status_code,response = get_user_details(email)
        if status_code == 200:
            user_type = response['type']
            if user_type == 2:
                course_list = []
                for j in batch_obj.courses.all():
                    course_list.append(j.name)
                batch_title = " & ".join(course_list) 
                
                nowDateTime = datetime.datetime.now()

                dec_meeting_license_number()

                batch_start_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")

                from datetime import timedelta
                batch_end_date_time = nowDateTime+timedelta(minutes=180)
                batch_end_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                meeting_responce,zoom_password_random = zoom_scheduled_meeting(request,title=batch_title,description=None,start=batch_start_date_time,end=batch_end_date_time,attendees_list=None,zoom_user_email = email)
            elif user_type == 1:
                license_obj = ZoomLicenseDetails.objects.all().last()
                total_license = license_obj.total_license
                use_license = license_obj.use_license

                free_license = int(total_license) - int(use_license)
                if free_license > 0:
                    responce = assign_license_to_user(email)
                    check_licence_response = get_user_details(email)
                    user_type = check_licence_response[1]['type']

                    if user_type == 2:
                        dec_meeting_license_number()
                        if responce == 204:
                            course_list = []
                            for j in batch_obj.courses.all():
                                course_list.append(j.name)
                            batch_title = " & ".join(course_list) 
                            
                            nowDateTime = datetime.datetime.now()

                            batch_start_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                            print("Batch Start Datetime Zoom Format : ",batch_start_date_time)

                            from datetime import timedelta
                            batch_end_date_time = nowDateTime+timedelta(minutes=180)
                            batch_end_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                            print("Batch end Datetime Zoom Format : ",batch_end_date_time)

                            print("******NOTE: CREATING MEETING FOR USER AFTER LICENSED")
                            meeting_responce,zoom_password_random = zoom_scheduled_meeting(request,title=batch_title,description=None,start=batch_start_date_time,end=batch_end_date_time,attendees_list=None,zoom_user_email = email)
                            print("******NOTE: MEETING CREATING SUCCEFULLY....")
                        else:
                            ctx['code'] = 0
                            ctx['error'] = "Meeting is not creating because licence is not free at this time..."
                    else:
                        ctx['code'] = 0
                        ctx['error'] = "No free licence is available on zoom..."
                else:
                    ctx['code'] = 0
                    ctx['error'] = "Licence is not free at this time...."
            else:
                ctx['error'] = "Error With User on Zoom Site..."

            if meeting_responce:
                meeting_id = meeting_responce['id']
                zoom_inst_url = meeting_responce['start_url']
                zoom_stu_url = meeting_responce['join_url']

                # instructor_meeting_link_bitly = genrate_bitly_link(request,zoom_inst_url)
                instructor_meeting_link_bitly = zoom_inst_url
                # student_meeting_link_bitly = genrate_bitly_link(request,zoom_stu_url)
                student_meeting_link_bitly = zoom_stu_url

                Batches.objects.filter(id=batch_id).update(
                    zoom_meeting_id = meeting_id,
                    zoom_meeting_password = zoom_password_random,
                    zoom_bitly_link_instructer = instructor_meeting_link_bitly,
                    zoom_bitly_link_student_mobile = student_meeting_link_bitly,
                    zoom_response_logs = meeting_responce
                )

                print("Batch Updated....")


                x = ZoomMeetingIdUserBatch(
                    meeting_type = 1,
                    batch_id = batch_id,
                    meeting_id = meeting_id,
                    meeting_status = '1',
                    zoom_meeting_password = zoom_password_random,
                    zoom_bitly_link_instructer = instructor_meeting_link_bitly,
                    zoom_bitly_link_student_mobile = student_meeting_link_bitly,
                    zoom_response_logs = meeting_responce,
                    meeting_start_at = datetime.datetime.now(),
                )
                x.save()

                print("Meeting Log created....")

                ctx['code'] = 1
                ctx['success'] = "yes"
                ctx['inst_link'] = instructor_meeting_link_bitly
        else:
            ctx['code'] = 0
            ctx['error'] = "Error to get your details from zoom server or user may be not registered on zoom"
    else:
        ctx['code'] = 0
        ctx['error'] = "Batch id is invalid..."
    return JsonResponse(ctx)


def recording_buy(request):
    
    pcid=request.GET.get('pcid', None)
    course_detail=Courses.objects.filter(id=pcid).first()
    cv=Recorded_Courses_name.objects.filter(course_id=pcid)
    # for j in course_detail:
    #     scourse=j.name
    #     price=j.price
    # print('P'*100)
    # print(scourse,price)
    # username = request.user.username
    # usernames = request.user.name
    # print(username)
    # print(usernames)
    return render(request, "classroom/recording_buy.html", {'course_detail':course_detail,'cv':cv})   


def paymentSuccess(request):
    crname=request.GET.get('crname', None)
    crprice=request.GET.get('crprice', None)
    pcid=request.GET.get('pcid', None)
    cv=Recorded_Courses_name.objects.filter(course_id=pcid)
    for i in cv:
        print(i.id,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    print(pcid,'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
    print('*'*100)
    print(crname)
    print(crprice)
    useremail = request.user.username
    username = request.user.name
    userid = request.user.id
    print(username)
    print(useremail)
    print(userid)
    userDetail=temp_recored_detail.objects.create(user=username,course=crname,price=crprice, email=useremail)
    purchseddetail=Purchased_classroom_recording_course.objects.create(user_id=userid, course_name_id=i.id )
    return render(request, "classroom/paysuccess.html")   

def demo_play(request):
    ctx={}
    cid = request.GET.get('cid', None)
    if cid:
        ct=Courses.objects.filter(id=cid).first()
        if ct:
            ctx['course']=ct.title
            
            video_link=DemoSaveVideo.objects.filter(course_name_id=cid).first()
            url='/media/'+str(video_link.video_uload)
            ctx['video_link']=video_link
            # print('00'*50)
            # print(video_link.video_uload)
                
                
            # ACCESS_KEY = settings.ACCESS_KEY
            # SECRET_KEY = settings.SECRET_KEY
            # BUCKETNAME = settings.BUCKETNAME

            # s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,config=Config(signature_version='s3v4'))

            # prefolder='democlass/'+str(cid)+str('/')
            # response = s3.list_objects_v2(Bucket=BUCKETNAME, Prefix=prefolder)
            # if 'Contents' in response:
            #     class_link = response["Contents"]
            #     class_link=class_link[0]['Key']
                
            #     # print("Class Link", class_link)
            #     # print('poih'*100)
                
            # else:
            #     print('video not found')
            
            # url = ''
            # class_link = class_link.replace("@",'/')

            # expiration=3600
            # # bucket_name = BUCKETNAME
            # object_name = class_link

            # # s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
            # try:
            #     response = s3.generate_presigned_url('get_object',Params={'Bucket': BUCKETNAME,'Key': object_name},ExpiresIn=expiration)
            #     url = response
            #     # print(response)
            # except Exception as e:
            #     print(e)
            # # print("123456"*100)
            # print(url)
            # print('pokj'*100)
            ctx['url'] = url
            ctx['base_url'] = settings.BASE_URL
                    
            return render(request,'classroom/demo_video_play.html',ctx)
        else:
            return render(request,"v4_home/error_course_not_found.html")
    else:
        return render(request,"v4_home/error_course_not_found.html")

@csrf_exempt
def availCourse(request):
    if request.method == "POST":
        cid = request.POST.get("courseid",None)  
        cr_obj=Courses.objects.filter(id=cid).last()
        crid=cr_obj.anquira_course.id
        try: 
            enq_onj=Enquiries(full_name = request.user.first_name, email = request.user.email)
            enq_onj.save()
            EnquiryCourses.objects.create(enquiry_id_id = enq_onj.id, courses_id =crid)
        except Exception as e:
            print(e)
    return render(request ,'classroom/classroom.html')

