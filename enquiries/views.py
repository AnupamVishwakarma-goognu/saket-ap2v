from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from courses.models import Courses
from .models import (
    #EnquiryCourses, InformationSharingTemplate,StudentResponse,EduzillaComments
    EnquiryCourses,StudentResponse,EduzillaComments
)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from anquira_v2.anquira_handlers import (
    DayOfWeekChoices, ReferenceModeChoices, TrainingModeChoices,
    EnquiryLevelChoices, AssignedByChoices
)
import json
from django.core import serializers
from django.views.generic import View, ListView
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from pure_pagination.mixins import PaginationMixin
from django.core.mail import EmailMessage
from .filters import EnquiryFilter
from users.models import CustomUserModel,CounselorPreferences
import csv
from datetime import datetime,time
from django.conf import settings
from activity.views import log_activity
from anquira_v2 import choices
import requests
from anquira_v2.utils import tat_algorithm,get_reference_for_csv,render_to_pdf
import logging
logger = logging.getLogger('second_log')
from anquira_v2.decorators import custome_check
from users.views import logout
from core.models import CountryCode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from payment.models import Order_plan_details
@csrf_exempt
def create_enquiry_api(request):
    if request.method == 'POST' and request.POST.get('key')==settings.API_KEY:
        print(request.POST.get('reference',False))
        ref = request.POST.get('reference',False)
        if "ap2vnoida.training" in ref or "ap2vgurgaon.training" in ref:
            print("-------------")
            try:
                page_ms2=request.POST['page_ms2']
            except:
                try:
                    logger.info("Reference: "+ request.POST.get('reference',False)+ ", Name: "+request.POST.get('name',False)+", Email: "+request.POST.get('email',False)+", Mobile: " +request.POST.get('mobile',False))
                    # logger.info("REFERENCE")
                except Exception as e:
                    print(e)
                return JsonResponse({"result": False}, status=500)
            if page_ms2:
                try:
                    logger.info("Reference: "+ request.POST.get('reference',False)+ ", Name: "+request.POST.get('name',False)+", Email: "+request.POST.get('email',False)+", Mobile: " +request.POST.get('mobile',False))
                    # logger.info("REFERENCE")
                except Exception as e:
                    print(e)
                return JsonResponse({"result": False}, status=500)
        sip = request.POST.get('source_ip',False)
        try:
            courses = request.POST.get('course','139')
            print(courses)
            if courses:
                courses = courses.split(',')

            """
            # commented by ashu
            cd = str(datetime.now().date())
            sd = cd+" 00:00:00"
            ed = cd+" 11:59:59"

            sd = datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
            ed = datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")
            
            # enquiries_queryset = Enquiries.objects.filter(source_ip = request.POST.get('source_ip','0.0.0.0'),mobile=request.POST.get('mobile','1234567890'))
            # eq = Enquiries.objects.filter(source_ip = request.POST.get('source_ip','0.0.0.0'),mobile=request.POST.get('mobile','1234567890'))
            eq = Enquiries.objects.filter(added_on__date__range = (sd,ed))
            # print(eq)

            if eq:
                enquiries_queryset = eq.filter(source_ip = request.POST.get('source_ip','0.0.0.0'),mobile=request.POST.get('mobile','1234567890'))
            
            if enquiries_queryset:
                return JsonResponse({"result": False}, status=500)
            """

            #Fetch all perameters form API hit and assing to eng variable then save.
            enq=Enquiries()
            reference=request.POST.get('reference',False)
            if reference:
                enq.reference=reference

            fullname=request.POST.get('name',False)
            if fullname:
                enq.full_name=fullname

            email=request.POST.get('email',False)
            if email:
                enq.email=email.lower()

            con_code=request.POST.get('con_code',False)
            if con_code:
                enq.country_code=con_code

            mobile=request.POST.get('mobile',False)
            enq.mobile=mobile

            training_mode=request.POST.get('mode',False)
            if training_mode:
                enq.training_mode=training_mode

            source_ip = request.POST.get('source_ip',False)
            if source_ip:
                enq.source_ip = source_ip

            comments = request.POST.get('comments',False)
            if comments:
                enq.comments = comments
            
            calling_datetime = request.POST.get('datetime',False)
            if calling_datetime:
                enq.calling_datetime = calling_datetime
            
            message = request.POST.get('message',False)
            if message:
                enq.message = message
            
            if CounselorPreferences.objects.filter(user__is_active=True).count() > 0:
                get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                if Enquiries.objects.filter(Q(email=email) | Q(mobile=mobile)):
                    enq_obj = Enquiries.objects.filter(Q(email=email) | Q(mobile=mobile)).last()
                    counselor = enq_obj.assigned_by.id

                    if CounselorPreferences.objects.filter(user = counselor):
                        # print("++++++++++++++++++++++++++++++++++++++++Yes")
                        enq.assigned_by = CustomUserModel.objects.get(id=counselor)
                    else:
                        # print("----------------------------------------No")
                        if get_counselor is not None:
                            enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                            CounselorPreferences.objects.filter(id=get_counselor.id).update(
                                last_assigned=True
                            )
                        else:
                            all_counselor = CounselorPreferences.objects.all()
                            for i in all_counselor:
                                CounselorPreferences.objects.filter(id=i.id).update(
                                last_assigned=False
                                )
                            # CounselorPreferences.objects.filter(id__in=all_counselor).update(last_assigned=False)
                            get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                            if get_counselor is not None:
                                enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                                CounselorPreferences.objects.filter(id=get_counselor.id).update(
                                    last_assigned=True
                                )
                            else:
                                all_counselor = CounselorPreferences.objects.all()
                                for i in all_counselor:
                                    CounselorPreferences.objects.filter(id=i.id).update(
                                    last_assigned=False
                                    )
                                # CounselorPreferences.objects.filter(id__in=all_counselor).update(last_assigned=False)
                                get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                                enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                                CounselorPreferences.objects.filter(id=get_counselor.id).update(
                                    last_assigned=True
                                )
                
                else:
                    if get_counselor is not None:
                        enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                        CounselorPreferences.objects.filter(id=get_counselor.id).update(
                            last_assigned=True
                        )
                    else:
                        all_counselor = CounselorPreferences.objects.all()
                        for i in all_counselor:
                            CounselorPreferences.objects.filter(id=i.id).update(
                            last_assigned=False
                            )
                        # CounselorPreferences.objects.filter(id__in=all_counselor).update(last_assigned=False)
                        get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                        if get_counselor is not None:
                            enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                            CounselorPreferences.objects.filter(id=get_counselor.id).update(
                                last_assigned=True
                            )
                        else:
                            all_counselor = CounselorPreferences.objects.all()
                            for i in all_counselor:
                                CounselorPreferences.objects.filter(id=i.id).update(
                                last_assigned=False
                                )
                            # CounselorPreferences.objects.filter(id__in=all_counselor).update(last_assigned=False)
                            get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                            enq.assigned_by = CustomUserModel.objects.get(id=get_counselor.user.id)
                            CounselorPreferences.objects.filter(id=get_counselor.id).update(
                                last_assigned=True
                            )

            enq.save()
            data =enq
            if courses:
                for course in courses:
                    coursedata_id = Courses.objects.filter(id = course).last()
                    if coursedata_id:
                        EnquiryCourses.objects.create(enquiry_id_id = data.id, courses_id = coursedata_id.id)
                    else:
                        print("Course not found for course_id:",course)
            # for course in selectCourses:
            #     c_obj = Courses.objects.get(id = course)
            #     enquirydata.courses.add(c_obj)
            #     enquirydata.save()
            return JsonResponse({"result": True, "id": data.id}, status=200)
        except Exception as e:
            print(e)
        return JsonResponse({"result": False,"msg":'All field are required'}, status=500)
    return JsonResponse({"result": False}, status=500)

@login_required(login_url = '/')
@custome_check()
def enquiry(request):
    course = Courses.objects.all().order_by('name')
    if request.method == 'POST':
        courses = request.POST.getlist('course')
        selectCourses = courses[0].split(',')



        try:
            enq=Enquiries()
            reference=request.POST.get('reference',False)
            if reference:
                enq.reference=reference


            fullname=request.POST.get('fullname',False)
            if fullname:
                enq.full_name=fullname

            email=request.POST.get('email',False)
            if email:
                enq.email=email.lower()

            mobile=request.POST.get('mobile',False)
            mobile = mobile.split("#")
            enq.mobile=mobile[1]

            company=request.POST.get('company',False)
            if company:
                enq.company_name=company

            assigned_by=request.POST.get('assigned_by',False)
            if assigned_by:
                enq.assigned_by_id=assigned_by

            designation=request.POST.get('designation',False)
            if designation:
                enq.designation=designation

            training_mode=request.POST.get('training_mode',False)
            if training_mode:
                enq.training_mode=training_mode

            enquiry_level=request.POST.get('enquiry_level',False)
            if enquiry_level:
                enq.enquiry_level=enquiry_level


            interested_batch=request.POST.get('interested_batch',False)
            if interested_batch:
                interested_batch=True if request.POST.get('interested_batch', True) == True else False
                enq.interested_batch=interested_batch

            batch_days=request.POST.getlist('select_days')
            if batch_days:
                enq.batch_days=batch_days

            batch_time=request.POST.get('batch_time',False)
            if batch_time:
                enq.batch_time=batch_time

            branch_location=request.POST.get('branch_location',False)
            enq.branch_location=branch_location

            alternative_email=request.POST.get('alternative_email',False)
            if alternative_email:
                enq.alternative_email=alternative_email

            alternative_mobile=request.POST.get('alternative_mobile',False)
            if alternative_mobile:
                enq.alternative_mobile=alternative_mobile

            enq.save()
            data =enq
            for course in selectCourses:
                coursedata_id = Courses.objects.filter(id = course).last()
                if coursedata_id:
                    EnquiryCourses.objects.create(enquiry_id_id = data.id, courses_id = coursedata_id.id)
                else:
                    print("Course not found for course_id:",course)
            Enquiries.objects.filter(id = data.id).update(
                country_code = mobile[0]
            )
            # for course in selectCourses:
            #     c_obj = Courses.objects.get(id = course)
            #     enquirydata.courses.add(c_obj)
            #     enquirydata.save()
            try:
                log_activity(request,action=choices.Action.add_enquiry, action_detail=choices.ActionDetails.add_enquiry,id=data.id)
            except Exception as e:
                print(e)
            return JsonResponse({"result": True, "id": data.id}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"result": False}, status=500)
    all_users = CustomUserModel.objects.filter(is_staff=False, exist_employee=True)
    # if request.user.is_superuser is False:
    all_users = all_users.all()

    context_data = {
        'course': course,
        'ReferenceModeChoices': ReferenceModeChoices.choice,
        'TrainingModeChoices': TrainingModeChoices.choice,
        'EnquiryLevelChoices': EnquiryLevelChoices.choice,
        # 'AssignedByChoices': AssignedByChoices.choice
        'AssignedByUser': all_users,
        'mindate':datetime.now().strftime( '%Y-%m-%d')
    }
    return render(request, 'enquiries/enquiry.html', context_data)

@login_required(login_url = '/')
@custome_check()
def update_enquiry(request, enquiry_update_id):
    if request.method == "POST":
        # print("----------------------------------------")
        # print(request.user.id)
        try:
            enq = Enquiries.objects.get(id = enquiry_update_id)
            reference=request.POST.get('reference',False)
            if reference:
                enq.reference=reference


            fullname=request.POST.get('fullname',False)
            if fullname:
                enq.full_name=fullname

            email=request.POST.get('email',False)
            if email:
                enq.email=email
            
            con_code = request.POST.get('con_code',None)
            if con_code:
                enq.country_code = con_code

            mobile=request.POST.get('mobile',False)
            enq.mobile=mobile

            company=request.POST.get('company',False)
            if company:
                enq.company_name=company

            assigned_by=request.POST.get('assigned_by',False)
            if assigned_by:
                enq.assigned_by_id=assigned_by
            else:
                enq.assigned_by_id=request.user.id

            designation=request.POST.get('designation',False)
            if designation:
                enq.designation=designation

            training_mode=request.POST.get('training_mode',False)
            if training_mode:
                enq.training_mode=training_mode

            enquiry_level=request.POST.get('enquiry_level',False)
            if enquiry_level:
                enq.enquiry_level=enquiry_level


            interested_batch=request.POST.get('interested_batch',False)
            if interested_batch:
                interested_batch=True if request.POST.get('interested_batch', True) == True else False
                enq.interested_batch=interested_batch

            batch_days=request.POST.getlist('select_days')
            if batch_days:
                enq.batch_days=batch_days

            batch_time=request.POST.get('batch_time',False)
            if batch_time:
                enq.batch_time=batch_time

            branch_location=request.POST.get('branch_location',False)
            enq.branch_location=branch_location

            alternative_email=request.POST.get('alternative_email',False)
            if alternative_email:
                enq.alternative_email=alternative_email

            alternative_mobile=request.POST.get('alternative_mobile',False)
            if alternative_mobile:
                enq.alternative_mobile=alternative_mobile

            enq.save()

            try:
                log_activity(request,action=choices.Action.mod_enquiry, action_detail=choices.ActionDetails.mod_enquiry,id=enquiry_update_id)
            except Exception as e:
                print(e)
            return JsonResponse({"result": True}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"result": False}, status=404)

@login_required(login_url = "/")
@csrf_exempt
def add_course(request, enquiries_id):
    if request.method == "POST":
        courseid = request.POST['courseid']
        enquiry_id = request.POST['enquiry_id']


        # delete "No course selected" if any single course associated
        has_no_course = EnquiryCourses.objects.filter(enquiry_id_id=int(enquiry_id), courses_id=settings.NO_COURSE_ID)
        if has_no_course:
            has_no_course.delete()

        EnquiryCourses.objects.create(enquiry_id_id=int(enquiry_id), courses_id=int(courseid))
        return JsonResponse({"result": enquiries_id}, status=200)

@login_required(login_url = '/')
@custome_check()
def discardCourse(request, enquiries_id):
    EnquiryCourseData = EnquiryCourses.objects.get(id = int(enquiries_id))
    reason=request.POST.get('reason','')
    # mark enquiry discard if all courses un/discard
    eid = EnquiryCourseData.enquiry_id.id
    e_obj = Enquiries.objects.get(id=eid)

    if EnquiryCourseData.status != EnquiryCourses.DISCARDED:
        EnquiryCourseData.status = EnquiryCourses.DISCARDED
        if reason:
            EnquiryCourseData.comment="{}:{}".format(datetime.now().strftime('%Y-%m-%d'),reason)
        EnquiryCourseData.save()

        #no need of this as everything is working on enquries
        # if not EnquiryCourses.objects.filter(enquiry_id=e_obj, discard=False).count():
        #     e_obj.discard = True
        #     e_obj.save()

    else:
        EnquiryCourseData.status = EnquiryCourses.NONE
        EnquiryCourseData.save()

        # # undiscard enquiry
        # if e_obj.discard:
        #     e_obj.discard = False
        #     e_obj.save()

    return JsonResponse({"result": True}, status=200)

def table_data_filter(request):
    if request.method == "GET":
        my_newdata = []
        filter_data = request.GET['filter_data']
        if len(filter_data) == 0:
            search_filter_data = Enquiries.objects.all()
            for i in search_filter_data:
                search_data_dict = {
                    "id": i.id,
                    "mobile": i.mobile,
                    "full_name": i.full_name,
                    "reference": i.reference,
                    "email": i.email,
                    "branch_location": i.branch_location
                }
                my_newdata.append(search_data_dict)
            return JsonResponse(my_newdata, status=200, safe=False)
        else:
            search_filter_data = Enquiries.objects.filter(Q(email__contains=filter_data) | Q(full_name__contains=filter_data) | Q(mobile__contains=filter_data) | Q(alternative_mobile__contains=filter_data) | Q(alternative_email__contains=filter_data))
            for i in search_filter_data:
                search_data_dict = {
                    "id": i.id,
                    "mobile": i.mobile,
                    "full_name": i.full_name,
                    "reference": i.reference,
                    "email": i.email,
                    "branch_location": i.branch_location
                }
                my_newdata.append(search_data_dict)
            return JsonResponse(my_newdata, status=200, safe=False)

@login_required(login_url="/")
def enquiries_filter(request):
    if request.method == "GET":
        search_data = request.GET['search_data']
        enquiries_filter_data = Enquiries.objects.filter(mobile__istartswith=search_data)
        context_data = {
            "enquiries_filter_data": enquiries_filter_data,
        }
        return render(request, 'enquiries/enquiry_filter.html', context_data)

@login_required(login_url = '/')
@custome_check()
def list_enquiry(request):
    course = Courses.objects.all().order_by('name')
    enquiries = Enquiries.objects.all().order_by('-id')
    if request.GET.get('type') and request.GET.get('n'):
        data = request.GET.copy()
        data.update(n={'type': request.GET.get('type'), 'n': request.GET.get('n')})
        enquiries = EnquiryFilter(data, enquiries).qs
    page = request.GET.get('page', 1)
    page_data = Paginator(enquiries, request=request)
    page_data.num_pages

    try:
        data = page_data.page(page)
    except PageNotAnInteger:
        data = page_data.page(1)
    except EmptyPage:
        data = page_data.page(page_data.num_pages)
    context_data = {
        "enquiries": data,
        "course": course
    }
    return render(request, 'enquiries/enquiry_list.html', context_data)

class EnquiryListView(PaginationMixin, ListView):
    object = Enquiries
    template_name = "enquiries/enquiry_list.html"
    paginate_by = 20
    course = Courses.objects.all().order_by('name')

    def get_queryset(self):
        # print("------------------------------------")
        
        name = self.request.GET.get('name',False)
        mobile = self.request.GET.get('mobile',False)
        email = self.request.GET.get('email',False)
        reference = self.request.GET.getlist('reference')
        course = list(map(int, self.request.GET.getlist('course')))
        owner = self.request.GET.get('owner',False)
        location = self.request.GET.get('location',False)
        start_date = self.request.GET.get('start_date',False)
        end_date = self.request.GET.get('end_date',False)
        training_mode = self.request.GET.get('training_mode',False)
        interest_level = self.request.GET.get('interest_level',False)
        interested_batch = self.request.GET.get('interested_batch',False)
        discarded = self.request.GET.get('discarded',False)
        enrolled = self.request.GET.get('enrolled',False)
        company_name = self.request.GET.get('company_name',False)
        designation = self.request.GET.get('designation',False)
        search = self.request.GET.get('search',False)

        
        # print('name : ',name)
        # print('mobile : ',mobile)
        # print('email : ',email)
        # print('reference : ',reference)
        # print('course : ',course)
        # print('owner : ',owner)
        # print('location : ',location)
        # print('start_date : ',start_date)
        # print('end_date : ',end_date)
        # print('training_mode : ',training_mode)
        # print('interest_level : ',interest_level)
        # print('interested_batch : ',interested_batch)
        # print('discarded : ',discarded)
        # print('company_name : ',company_name)
        # print('designation : ',designation)
        # print('search : ',search)

        request=self.request
        if search == "yes":
            request.session['enquiry_filter_data'] = {'name':name,'mobile':mobile,'email':email,'reference':reference,'course':course,'owner':owner,
                                                    'location':location,'start_date':start_date,'end_date':start_date,'training_mode':training_mode,
                                                    'interest_level':interest_level,'interested_batch':interested_batch,'discarded':discarded,'company_name':company_name,'designation':designation,
                                                    'enrolled':enrolled}
        else:
            request.session['enquiry_filter_data'] = ""
        # print(request.session['enquiry_filter_data']['name'])
        
            # print()
       
        unattended = self.request.GET.get('unattended',False)
        if unattended:
            enquiries = Enquiries.objects.filter(attended=0).order_by('-id').distinct()
        else:
            enquiries = Enquiries.objects.all().order_by('-id').distinct()

        # show = request.GET.get("show",None)
        # list1 = []
        # if show == "discard":
        #     for i in enquiries:
        #         enq_course_obj = EnquiryCourses.objects.filter(enquiry_id = i.id)
        #         status_list = []
        #         for j in enq_course_obj:
        #             status_list.append(int(j.status))
                
        #         if 2 not in status_list:
        #             list1.append(i.id)
        # elif show == "enrolled":
        #     for i in enquiries:
        #         enq_course_obj = EnquiryCourses.objects.filter(enquiry_id = i.id)
        #         status_list = []
        #         for j in enq_course_obj:
        #             status_list.append(int(j.status))
                
        #         if 1 not in status_list:
        #             list1.append(i.id)
        # else:
        #     for i in enquiries:
        #         enq_course_obj = EnquiryCourses.objects.filter(enquiry_id = i.id)
        #         status_list = []
        #         for j in enq_course_obj:
        #             status_list.append(int(j.status))
                
        #         if 0 not in status_list:
        #             list1.append(i.id)
        # enquiries = enquiries.exclude(id__in = list1)
        

        request_data = self.request.GET.copy()

        q_references=request.GET.getlist('reference')
        request_data['reference'] = ','.join(q_references)


        q_courses=request.GET.getlist('course')
        request_data['course'] = ','.join(q_courses)
        
        
        if request.GET.get('enrolled',False):
            enquiries = enquiries.filter(enquirycourses__status=EnquiryCourses.ENROLLED).distinct()
        if request.GET.get('discarded',False):
            enquiries = enquiries.filter(enquirycourses__status=EnquiryCourses.DISCARDED).distinct()

        # else:
        #     enquiries = enquiries.filter(enquirycourses__status=EnquiryCourses.NONE).distinct()
        enquiries = EnquiryFilter(request_data, enquiries).qs

        # print("----------------------------------------------------------------")
        # print(enquiries)
        return enquiries.order_by('-id')

    def get(self,*args,**kwargs):
        # print("+++++++++++++++++++++++++++++-")
        if self.request.user.is_active:
            if self.request.user.is_authenticated:
                if self.request.GET.get('download'):
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="enquiries.csv"'

                    writer = csv.writer(response)
                    writer.writerow(['Id',"Name",'Email','Phone','Branch Location','Mode'])
                    for item in self.get_queryset():
                        writer.writerow([item.id,item.full_name,item.email,item.mobile,item.branch_location,item.reference])
                        # writer.writerow(item)
                    return response
                return super().get(*args,**kwargs)
        else:
            if self.request.user.is_authenticated:
                logout(self.request)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/")

    def get_context_data(self, *args, **kwargs):
        # print("*****************************************")
        context = super().get_context_data(**kwargs)
        context['q_references'] = self.request.GET.getlist('reference')
        context['q_courses'] = list(map(int, self.request.GET.getlist('course')))
        context['enquiries'] = self.get_queryset()
        context['references']= ReferenceModeChoices.choice
        context['courses'] = Courses.objects.all().order_by('name')
        context['locations'] = Enquiries.BRANCH_LOCATION
        context['users'] = CustomUserModel.objects.filter(exist_employee=True)
        q_training_mode=self.request.GET.get('training_mode',False)
        context['q_training_mode'] = int(q_training_mode) if q_training_mode else ''
        q_interest_level = self.request.GET.get('interest_level',False)
        context['q_interest_level'] = int(q_interest_level) if q_interest_level else ''
        context['training_modes'] = TrainingModeChoices.choice
        context['interest_levels'] = EnquiryLevelChoices.choice
        return context


@login_required(login_url = '/')
@custome_check()
def view(request, enquiries_id):
    if not Enquiries.objects.filter(id = enquiries_id).first():
        ctx={}
        ctx['enquiry']=enquiries_id
        return render(request, 'enquiries/enquiry_error.html',ctx)
    enquiry = Enquiries.objects.get(id = enquiries_id)
    EnquireCourseData = EnquiryCourses.objects.filter(enquiry_id_id = enquiries_id)
    # allselectdata = enquiry.courses.get_queryset()
    # tomorrow=datetime.now() + timedelta(days=1)
    tomorrow = datetime.combine(datetime.now(), time.max)
    #@@followups = Followups.objects.filter(followupid=enquiries_id).order_by('-next_followup')
    followups = Followups.objects.filter(followupid=enquiries_id).order_by('-added_on')
    next_followup=Followups.objects.filter(followupid=enquiries_id,next_followup__gte=tomorrow).order_by('next_followup').first()
    pay_link=Order_plan_details.objects.filter(email=enquiry.email)
    for z in pay_link:
        amount=z.amount
    if pay_link:
        yes= True
       
    else:
        yes=False
        amount=0
        
   
    context_data = {
        "enquiry": enquiry,
        "working_days": enquiry.batch_days.split(','),
        "days_of_week_all": DayOfWeekChoices.choice,
        "followups": followups,
        'EnquireCourseData': EnquireCourseData,
        'courses': Courses.objects.all().order_by('name'),
        'selected_courses':Courses.objects.filter(id__in=EnquireCourseData.values_list('courses_id',flat=True)),
        'ReferenceModeChoices': ReferenceModeChoices.choice,
        'TrainingModeChoices': TrainingModeChoices.choice,
        'EnquiryLevelChoices': EnquiryLevelChoices.choice,
        # 'AssignedByChoices': AssignedByChoices.choice
        'AssignedByUser': CustomUserModel.objects.filter(is_staff=False, exist_employee=True),
        'mindate':datetime.now().strftime( '%Y-%m-%d'),
        'student_responses': StudentResponse.objects.all().order_by('priority'),
        'maxdate':(next_followup.next_followup - timedelta(days=1)).strftime( '%Y-%m-%d') if next_followup else '',
        'pay':yes,
        'amount':amount
    }

    email = enquiry.email
    mobile = enquiry.mobile
    # print(mobile)
    # print("-------")
    if mobile:
        mobile = mobile.strip(" ")
    if email and mobile:
        enq_obj = Enquiries.objects.filter(Q(email=email) | Q(mobile=mobile))
        if enq_obj.count()>=2:
            context_data['enq_obj']=enq_obj
    elif mobile:
        enq_obj = Enquiries.objects.filter(mobile=mobile)
        if enq_obj.count()>=2:
            context_data['enq_obj']=enq_obj
    elif email:
        enq_obj = Enquiries.objects.filter(email=email)
        if enq_obj.count()>=2:
            context_data['enq_obj']=enq_obj
    context_data['con_codev'] = CountryCode.objects.all()

    return render(request, 'enquiries/view.html', context_data)

@login_required(login_url = '/')
@custome_check()
@csrf_exempt
def addFollowUps(request, followup_id):
    follows = Followups.objects.filter(followupid_id = followup_id)
    enquiry = Enquiries.objects.get(id = followup_id)

    # mark the enquiry attended
    if not enquiry.attended:
        enquiry.attended = True
        enquiry.save()

    if request.method == 'POST':
        followups_mode = request.POST['followups_mode']
        # response = request.POST['response']
        next_followup = request.POST['next_followup']
        comment = request.POST['comment']
        source_page = request.POST.get("source_page", False)
        #update all existing followup as done and create new one
        now= datetime.now()
        #At the time of new follow up, all existing follow ups will be marked complete
        Followups.objects.filter(followupid_id=enquiry.id).update(is_complete=True)
        Followups.objects.get_or_create(
            followupid_id = enquiry.id,
            followup_mode = followups_mode,
            # response = response,
            next_followup = next_followup,
            comments = comment,
            assigned_user_id=request.user.id,
            student_response_id=request.POST.get('student_response',None)
        )
        #update next followup date in enquiry
        enquiry.next_followup=next_followup
        enquiry_course_obj = EnquiryCourses.objects.filter(enquiry_id_id = enquiry.id).last()
        print("------------------------------------------------------------------------")
        print(enquiry_course_obj)
        if enquiry_course_obj:
            if enquiry_course_obj.status == 2:              # 2 for discard
                enquiry.assigned_by_id=request.user.id
                EnquiryCourses.objects.filter(id = enquiry_course_obj.id).update(
                    status = 0
                )

        enquiry.save()

        try:
            log_activity(request,action=choices.Action.add_followup, action_detail=choices.ActionDetails.add_followup,id=enquiry.id)
        except Exception as e:
            print(e)

        

        if source_page:
            return HttpResponse('success')
        return HttpResponseRedirect('/enquiries/view/{thisisid}/'.format(thisisid = followup_id))
    context_data = {
        'follows': follows,
        'enquiry':enquiry,
        'ReferenceModeChoices': ReferenceModeChoices.choice,
        'TrainingModeChoices': TrainingModeChoices.choice,
        'AssignedByChoices': AssignedByChoices.choice,

    }
    return render(request, 'enquiries/view.html', context_data)


# def list_followups(request):
#     follows = Followups.objects.all()
#     return render(request, 'enquiries/view.html', {'follows': follows})

class DiscardFollowupsView(View):
    followup_model = Followups

    def post(self, *args, **kwargs):
        # print("kwargs",self.request.POST)
        reason=self.request.POST.get('reason','')
        response = {
            'status': 0
        }
        followup_obj = self.followup_model.objects.filter(
            id=self.kwargs.get('pk')
        )
        if followup_obj.exists():
            if followup_obj.first().discard:
                followup_obj.update(
                    discard=False
                )
            else:
                fl=followup_obj.first()
                fl.discard=True
                fl.comments = "{} Discard Reason:{}".format(fl.comments,reason)
                fl.save()
            response.update(
                status=1
            )
        return JsonResponse(response)


class DiscardEnquiryView(View):
    enquiry_model = Enquiries

    def post(self, *args, **kwargs):
        response = {
            'status': 0
        }
        enquiery_obj = self.enquiry_model.objects.filter(
            id=self.kwargs.get('pk')
        )
        if enquiery_obj.exists():
            # Followups.objects.filter(followupid=enquiery_obj.last()).update(discard=True)
            enq=enquiery_obj.first()
            if enq and enq.discard:
                enq.discard_action(new_discard_status=False)
            else:
                reason=self.request.POST.get('reason','')
                enq.discard_action(new_discard_status=True,reason=reason)
            response.update(status=1)

            # print("------------------------------------")
            # print(self.request.user)
        return JsonResponse(response)

"""
class CoursesContentSendView(View):
    def post(self, *args, **kwargs):
        response = {
            'status': 0
        }

        return JsonResponse(response)
"""

class CoursesContentSendView(View):
    enquiry_model = Enquiries
    courses_model = Courses
    email_template = InformationSharingTemplate.objects.filter(send_type=InformationSharingTemplate.EMAIL,type=InformationSharingTemplate.COURSE).last()
    sms_template = InformationSharingTemplate.objects.filter(send_type=InformationSharingTemplate.SMS,type=InformationSharingTemplate.COURSE).last()

    def send_mail_to_student(self, dict_data=None, *args, **kwargs):
        from django.conf import settings
        email = EmailMessage(
            self.email_template.subject,
            dict_data.get('body'),
            settings.EMAIL_HOST,
            [dict_data.get('email')],
        )
        if dict_data.get('image'):
            email.attach_file(settings.BASE_DIR + dict_data.get('image'))
        email.send()

    def send_sms_to_student(self, dict_data=None, *args, **kwargs):
        from django.conf import settings
        import requests
        url = settings.SMS_URL
        url=url.format(**dict_data)
        # print("final sms url",url)
        r=requests.get(url)

    def post(self, *args, **kwargs):
        response = {
            'status': 0
        }
        send_type = int(self.request.POST.get('send_type','1'))
        courses_obj = self.courses_model.objects.filter(
            id=self.request.POST.get('courses')
        )
        enquiry_obj = self.enquiry_model.objects.filter(
            id=self.kwargs.get('pk')
        )
        if courses_obj.exists() and enquiry_obj.exists():
            data_dict={}
            data_dict['username']=enquiry_obj.first().full_name.title(),
            data_dict['course_name']=courses_obj.first().name,
            data_dict['course_url']=courses_obj.first().url,
            data_dict['course_duration']=courses_obj.first().duration,
            data_dict['course_price']=courses_obj.first().price
            if send_type == InformationSharingTemplate.EMAIL and self.email_template:
                email_data = {
                    'body': self.email_template.body.format(**data_dict),
                    'email': enquiry_obj.first().email,
                    'image': courses_obj.first().course_content.url if courses_obj.first().course_content else None
                }
                self.send_mail_to_student(dict_data=email_data)
                response.update(status=1)
            elif send_type == InformationSharingTemplate.SMS and self.sms_template:
                d={}
                d['body'] = self.sms_template.body.format(**data_dict)
                d['mobile']=enquiry_obj.first().mobile
                self.send_sms_to_student(d)
                response.update(status=1)
        return JsonResponse(response)


class AccountDetailSendView(View):
    enquiry_model = Enquiries
    email_template = InformationSharingTemplate.objects.filter(send_type=InformationSharingTemplate.EMAIL,type=InformationSharingTemplate.ACCOUNT_DETAILS).last()
    sms_template = InformationSharingTemplate.objects.filter(send_type=InformationSharingTemplate.SMS,type=InformationSharingTemplate.ACCOUNT_DETAILS).last()

    def send_mail_to_student(self, dict_data=None, *args, **kwargs):
        from django.conf import settings
        email = EmailMessage(
            self.email_template.subject,
            dict_data.get('body'),
            settings.EMAIL_HOST,
            [dict_data.get('email')],
        )
        if dict_data.get('image'):
            email.attach_file(settings.BASE_DIR + dict_data.get('image'))
        email.send()

    def send_sms_to_student(self, dict_data=None, *args, **kwargs):
        from django.conf import settings
        import requests
        url = settings.SMS_URL
        url=url.format(**dict_data)
        # print("final sms url",url)
        r=requests.get(url)

    def post(self, *args, **kwargs):
        response = {
            'status': 0
        }
        send_type = int(self.request.POST.get('send_type','1'))
        enquiry_obj = self.enquiry_model.objects.filter(
            id=self.kwargs.get('pk')
        )
        if  enquiry_obj.exists():
            data_dict={}
            data_dict['username']=enquiry_obj.first().full_name.title(),
            if send_type == InformationSharingTemplate.EMAIL and self.email_template:
                email_data = {
                    'body': self.email_template.body.format(**data_dict),
                    'email': enquiry_obj.first().email,
                }
                self.send_mail_to_student(dict_data=email_data)
                response.update(status=1)
            elif send_type == InformationSharingTemplate.SMS and self.sms_template:
                d={}
                d['body'] = self.sms_template.body.format(**data_dict)
                d['mobile']=enquiry_obj.first().mobile
                self.send_sms_to_student(d)
                response.update(status=1)
        return JsonResponse(response)


@csrf_exempt
def eduzillacomment(request):
    uid=request.POST.get('id')
    stud_details=request.POST.get('stud_details')
    comments =request.POST.get('comments')
    ed,created=EduzillaComments.objects.get_or_create(uid=uid)
    ed.stud_details=stud_details
    ed.comments=comments
    ed.save()
    return JsonResponse({'status':'ok'})


def download_excel(request):
    enquires_queryset = Enquiries.objects.all()

    if request.session['enquiry_filter_data']:
        if request.session['enquiry_filter_data']['name']:
            enquires_queryset = enquires_queryset.filter(full_name = request.session['enquiry_filter_data']['name'])
        if request.session['enquiry_filter_data']['mobile']:
            enquires_queryset = enquires_queryset.filter(mobile = request.session['enquiry_filter_data']['mobile'])
        if request.session['enquiry_filter_data']['email']:
            enquires_queryset = enquires_queryset.filter(email = request.session['enquiry_filter_data']['email'])
        if request.session['enquiry_filter_data']['reference']:
            enquires_queryset = enquires_queryset.filter(reference = request.session['enquiry_filter_data']['reference'])
        if request.session['enquiry_filter_data']['start_date']:
            enquires_queryset = enquires_queryset.filter(added_on__gte = request.session['enquiry_filter_data']['start_date'])
        if request.session['enquiry_filter_data']['end_date']:
            enquires_queryset = enquires_queryset.filter(added_on__lte = request.session['enquiry_filter_data']['end_date'])
        if request.session['enquiry_filter_data']['training_mode']:
            enquires_queryset = enquires_queryset.filter(training_mode = request.session['enquiry_filter_data']['training_mode'])
        if request.session['enquiry_filter_data']['discarded']:
            enquires_queryset = enquires_queryset.filter(tmp_discard = request.session['enquiry_filter_data']['discarded'])
        

    if request.session['enquiry_filter_data']:
        print(request.session['enquiry_filter_data']['name'])
    
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['SrNo','ID','Name','Email','Phone','Reference','Added By','Date'])

    n = 1
    for i in enquires_queryset:
        row = (
            n,
            i.id,
            i.full_name,
            i.email,
            i.mobile,
            get_reference_for_csv(request,i.reference),
            i.assigned_by,
            i.added_on,
        )
        n=n+1
        writer.writerow(row)

    response['Content-Disposition'] = 'attachment; filename=Enquires-{date}.csv'.format(date=datetime.now().strftime('%d-%m-%Y'),)
    return response
    # return HttpResponse("ok")


def download_pdf(request, *args, **kwargs):
    enquires_queryset = Enquiries.objects.all()

    if request.session['enquiry_filter_data']:
        if request.session['enquiry_filter_data']['name']:
            enquires_queryset = enquires_queryset.filter(full_name = request.session['enquiry_filter_data']['name'])
        if request.session['enquiry_filter_data']['mobile']:
            enquires_queryset = enquires_queryset.filter(mobile = request.session['enquiry_filter_data']['mobile'])
        if request.session['enquiry_filter_data']['email']:
            enquires_queryset = enquires_queryset.filter(email = request.session['enquiry_filter_data']['email'])
        if request.session['enquiry_filter_data']['reference']:
            enquires_queryset = enquires_queryset.filter(reference = request.session['enquiry_filter_data']['reference'])
        if request.session['enquiry_filter_data']['start_date']:
            sd = request.session['enquiry_filter_data']['start_date']+" 00:00:00"
            sd = datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
            enquires_queryset = enquires_queryset.filter(added_on__gte = sd)
        if request.session['enquiry_filter_data']['end_date']:
            ed = request.session['enquiry_filter_data']['end_date']+" 00:00:00"
            ed = datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")
            enquires_queryset = enquires_queryset.filter(added_on__lte = ed)
        if request.session['enquiry_filter_data']['training_mode']:
            enquires_queryset = enquires_queryset.filter(training_mode = request.session['enquiry_filter_data']['training_mode'])
        if request.session['enquiry_filter_data']['discarded']:
            enquires_queryset = enquires_queryset.filter(tmp_discard = request.session['enquiry_filter_data']['discarded'])

    pdf = render_to_pdf('enquiries/pdfgen.html', {'enquires_queryset':enquires_queryset})
    return HttpResponse(pdf, content_type='application/pdf')

def get_enquirie_details(request):
    ctx={}
    email = request.GET.get("email",None)
    mobile = request.GET.get("mobile",None)
    if email and mobile:
        enq_obj = Enquiries.objects.filter(Q(email=email) | Q(mobile=mobile))
        ctx['enq_obj']=enq_obj
    elif mobile:
        enq_obj = Enquiries.objects.filter(mobile=mobile)
        ctx['enq_obj']=enq_obj
    elif email:
        enq_obj = Enquiries.objects.filter(email=email)
        ctx['enq_obj']=enq_obj
    if enq_obj:
        return render(request,'enquiries/duplicate_enquiry_modal.html',ctx)
    else:
        return JsonResponse({"code":201})

def mark_as_junk(request):
    ctx={}
    enq_id = request.GET.get("enq_id",None)
    if enq_id:
        enquiries_obj = Enquiries.objects.filter(id=enq_id).first()
        if enquiries_obj:
            Enquiries.objects.filter(id=enq_id).update(
                junk=True
            )
    return JsonResponse({"code":200})

def mark_as_real(request):
    ctx={}
    enq_id = request.GET.get("enq_id",None)
    if enq_id:
        enquiries_obj = Enquiries.objects.filter(id=enq_id).first()
        if enquiries_obj:
            Enquiries.objects.filter(id=enq_id).update(
                junk=False
            )
    return JsonResponse({"code":200})

def send_introduction_email(request):
    data = {}
    enq_id = request.POST.get("enq_id",None)
    epassword = request.POST.get("email_p",None)

    if enq_id and epassword:
        enq_obj = Enquiries.objects.filter(id=enq_id).first()
        if enq_obj:
            try:
                 email = enq_obj.email
            except Exception as e:
                print(e)
                return JsonResponse({},status=400)
            if email:
                html_content=render_to_string('email_templates/onlinetraning.html', data)
                text_content=html_content
            
                settings.EMAIL_HOST_PASSWORD = str(epassword)

                msg = EmailMultiAlternatives('AP2V Academy ', text_content, "AP2V Academy", [email])
                msg.attach_alternative(html_content, "text/html")
                status=msg.send()
                print("Email Send")

                return JsonResponse({},status=200)
            else:
                return JsonResponse({},status=400)
        else:
            return JsonResponse({},status=400)
    else:
        return JsonResponse({},status=400)






def add_enquiry_modal(request):
    course = request.GET.get("course",139)
    mode = request.GET.get("mode",None)
    name = request.GET.get("name",None)
    email = request.GET.get("email",None)
    mobile = request.GET.get("mobile",None)
    designation = request.GET.get("designation",None)
    batch_preference = request.GET.get("batch_preference",None)
    batch_time = request.GET.get("batch_time",None)
    interest_for_batch = request.GET.get("interest_for_batch",None)
    alt_email = request.GET.get("alt_email",None)
    alt_mobile = request.GET.get("alt_mobile",None)

    course = course.split(",")
    batch_preference = batch_preference.split(",")


    x = Enquiries(reference = mode, full_name=name, email=email, 
                    mobile=mobile, designation=designation, 
                    batch_days =batch_preference,interested_batch=int(interest_for_batch),
                    alternative_email=alt_email,alternative_mobile= alt_mobile,
                    assigned_by_id = request.user.id
                    )
    x.save()
    try:
        if course:
            for cou in course:
                coursedata_id = Courses.objects.filter(id = cou).last()
                if coursedata_id:
                    EnquiryCourses.objects.create(enquiry_id_id = x.id, courses_id = coursedata_id.id)
                else:
                    print("Course not found for course_id:",cou)
        return JsonResponse({"result": True, "id": x.id}, status=200)
    except Exception as e:
        print(e)
    return JsonResponse({"result": False}, status=500)


def get_unattended_enq(request):
    data={}
    enq = Enquiries.objects.filter(attended=0).count()
    # print(enq)
    data['count'] = enq
    return JsonResponse(data,status=200)