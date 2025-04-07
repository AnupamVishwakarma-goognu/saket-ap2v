from operator import imod
from traceback import print_tb
from webbrowser import get
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import Batches,BestRecording,BatchSessionOff,PublicHoliday,ZoomMeetingIdUserBatch,ZoomWeebHookResponce,StudentCertificateIssued
from courses.models import Courses
from instructors.models import Instructors
from enrolls.models import Enrollments
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from anquira_v2 import anquira_handlers, choices
from django.views.generic import View
from django.views.generic.edit import (
    UpdateView
)
from datetime import datetime, timedelta
from .filters import BatchesFilter
from django.core.paginator import Paginator
from activity.views import log_activity
from bluejeans.views import scheduled_meeting,genrate_bitly_link
from django.conf import settings
from chats.views import create_room_api
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings
from communication.views import SendSMS,send_batch_invite_email,send_batch_off_reminder,sending_holiday_email
from enquiries.models import Enquiries, EnquiryCourses
import calendar
from demo.models import Demo
from users.models import CustomUserModel as User
from instructors.models import Instructors
from django.views.decorators.csrf import csrf_exempt

import urllib
import requests
import shutil
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError
import os
import datetime
import re
from collections import OrderedDict
from classroom.models import BatchStudentFeedback
from anquira_v2.decorators import custome_check 
from django_chatter.models import Room
import json
from bluejeans.zoom import remove_license_to_user,inc_meeting_license_number
from django.shortcuts import get_object_or_404
from django.db import transaction


# @login_required(login_url = '/')
# @custome_check()
# def batches(request):
#     from datetime import datetime
#     if request.method == 'POST':
#         bname = "btch-{autogen}".format(autogen = anquira_handlers.get_batch_name())
#         candidate_data = request.POST['candidate'].split(',')
#         if candidate_data[-1]=="":
#             candidate_data.pop()
#         candidate_data2 = request.POST['candidate2'].split(',')
#         if candidate_data2[-1]=="":
#             candidate_data2.pop()
#         print(f"{candidate_data} candidate2: {candidate_data2}")
#         candidate_data = candidate_data+candidate_data2
#         candidate_data = list(dict.fromkeys(candidate_data))

#         days_of_week = ",".join(request.POST.getlist('days_of_week'))
#         start_date_time = request.POST['start_date_time']
#         start_date_time = datetime.strptime(start_date_time, '%m/%d/%Y %I:%M %p')
#         instructors = request.POST['instructors']
#         session_duration = request.POST['session_duration']
#         batch_type = request.POST['batch_type']
#         language_type = request.POST['language_type']
#         courses_id = Courses.objects.get(id = int(request.POST['course'])).id
#         print("Course ID : ",courses_id)
#         try:
#             complete = request.POST('complete')
#         except:
#             complete = 'False'
#         courses_id_list = ",".join(request.POST.getlist('course'))
#         print("Courses ID List : ",courses_id_list)
#         duration = Courses.objects.get(id = int(courses_id)).duration
#         candidate = ""
#         candidate_extend_list = []
#         for candidate_details in candidate_data:
#             candidate_extend_list.append(Enrollments.objects.get(id = int(candidate_details)).enquiry_course_id.enquiry_id.full_name)
#         print("Candidate Extend List : ",candidate_extend_list)
#         candidate = ", ".join(candidate_extend_list)
#         end_date_time = request.POST.get('end_date_time')
#         end_date_time = datetime.strptime(end_date_time, '%m/%d/%Y %I:%M %p')
#         courses_id_list = courses_id_list.split(",")

#         end_date_time2 = end_date_time+timedelta(days=100)

#         attendees_data = []
#         room_emails = [] 
#         print("---------Candidate Data 96 :----------- ",candidate_data)
#         for i in candidate_data:
#             print("i: ",i)
#             attendees_email={}
#             enroll_students = Enrollments.objects.get(id = int(i))
#             email = enroll_students.enquiry_course_id.enquiry_id.email
#             attendees_email['email'] = email
#             room_emails.append(email)
#             attendees_data.append(attendees_email)

#         instructors_obj = Instructors.objects.filter(id = instructors).first()
#         user_id = None
#         moderator_passcode = settings.MODERATOR_PASSCODE
#         if instructors_obj.blue_jeans_user_id:
#             user_id = instructors_obj.blue_jeans_user_id
#             moderator_passcode = instructors_obj.blue_jeans_passcode

#         title = Courses.objects.get(id = int(courses_id_list[0])).name+" Batch"
#         meeting_id = '0000000'
#         attendees_passcode = True
#         student_meeting_link = True
#         instructor_meeting_link = True
        
        
#         if meeting_id and attendees_passcode and moderator_passcode:
#             create_batch = Batches.objects.create(batch_name=bname, days_of_week=days_of_week, duration=duration,
#                             start_date_time=start_date_time, instructors_id=int(instructors),instructor_blue_jeans_user_id=user_id,
#                             session_duration=session_duration, candidates=candidate, complete=complete,
#                             meeting_id = meeting_id,moderator_passcode=moderator_passcode,attendee_passcode=attendees_passcode,
#                             bitly_link_instructer = instructor_meeting_link,bitly_link_student_mobile=student_meeting_link,end_date_time=end_date_time,batch_type=batch_type,language_type=language_type)
            
#             enrolled_course_id_list = []
#             for m in courses_id_list:
#                 courses_id=Courses.objects.get(id = int(m)).id
#                 enrolled_course_id_list.append(courses_id)
#             create_batch.courses.set(enrolled_course_id_list)
            
#             enrolled_student_id_list = []
#             print("---------Candidate Data 134 :----------- ",candidate_data)
#             for i in candidate_data:
#                 enroll_students = Enrollments.objects.get(id = int(i))
#                 enroll_students.batch = create_batch.id
#                 enroll_students.save()
#                 enrolled_student_id_list.append(enroll_students.id)
#             create_batch.enroll_student.set(enrolled_student_id_list)
#             print("enrolled_student_id_list: ",enrolled_student_id_list)
#             course_name = Courses.objects.filter(id = int(courses_id_list[0])).first().name
#             print("Sending Email.....Batch")
#             send_batch_invite_email(request,course_name,start_date_time,student_meeting_link,enrolled_student_id_list)
            
#             try:
#                 log_activity(request,action=choices.Action.add_batch, action_detail=choices.ActionDetails.add_batch,id=create_batch.id)
#             except Exception as e:
#                 print(e)

#         room_emails.append(instructors_obj.email)
#         data = create_room_api(request,room_emails)
#         print("Room id: ",data['room_id'])
#         if data['room_id']:
#             Batches.objects.filter(id=create_batch.id).update(
#                 chat_room_id = data['room_id'])
#         return redirect(reverse('batchlist'))

#     context_data = {
#         'instructor': Instructors.objects.filter(active=True),
#         'enrollment': Enrollments.objects.all(),
#         'course': Courses.objects.all().order_by('name'),
#         'mindate':datetime.now().strftime( '%Y-%m-%d')
#     }
#     return render(request, 'batches/batches_form.html', context_data)

@login_required(login_url = '/')
@custome_check()
def batches(request):
    from datetime import datetime, timedelta

    if request.method == 'POST':
        bname = "btch-{autogen}".format(autogen=anquira_handlers.get_batch_name())

        candidate_data = request.POST['candidate'].split(',')
        if candidate_data[-1] == "":
            candidate_data.pop()
        candidate_data2 = request.POST['candidate2'].split(',')
        if candidate_data2[-1] == "":
            candidate_data2.pop()

        candidate_data = list(dict.fromkeys(candidate_data + candidate_data2))  # Remove duplicates

        days_of_week = ",".join(request.POST.getlist('days_of_week'))
        start_date_time = datetime.strptime(request.POST['start_date_time'], '%m/%d/%Y %I:%M %p')
        instructors = request.POST['instructors']
        session_duration = request.POST['session_duration']
        batch_type = request.POST['batch_type']
        language_type = request.POST['language_type']
        # print("language_type: ",language_type)
        # print("batch_type: ",batch_type)
        # print("session_duration: ",session_duration)
        # print("instructors: ",instructors)
        # print("days_of_week: ",days_of_week)
        # print("start_date_time: ",start_date_time)

        courses_id = Courses.objects.get(id=int(request.POST['course'])).id
        # print("Course ID : ",courses_id)
        complete=False
        try:
            complete = request.POST['complete']
        except KeyError:
            complete = 'False'

        duration = Courses.objects.get(id=int(courses_id)).duration
        candidate_extend_list = []


        for candidate_id in candidate_data:
            enrollment = get_object_or_404(Enrollments, id=int(candidate_id))
            enquiry = enrollment.enquiry_course_id.enquiry_id 
            email = enquiry.email
            mobile = enquiry.mobile

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': enquiry.full_name.split()[0] if enquiry.full_name else '',
                    'last_name': ' '.join(enquiry.full_name.split()[1:]) if len(enquiry.full_name.split()) > 1 else '',
                    'mobile': enquiry.mobile,
                    'user_type': 'student',
                    'is_active': True
                }
            )
            user.set_password(str(email)+str(mobile))
            user.save()
            if created:
                print(f"New user created: {user.email}")

            candidate_extend_list.append(enquiry.full_name)

        candidate = ", ".join(candidate_extend_list)

        end_date_time = datetime.strptime(request.POST.get('end_date_time'), '%m/%d/%Y %I:%M %p')
        courses_id_list = request.POST.getlist('course')
        # print("end_date_time: ", end_date_time)
        # print("courses_id_list: ", courses_id_list)
        # print("candidate: ",candidate)
        with transaction.atomic():
            create_batch = Batches.objects.create(
                batch_name=bname,
                days_of_week=days_of_week,
                duration=duration,
                start_date_time=start_date_time,
                instructors_id=int(instructors),
                session_duration=session_duration,
                candidates=candidate,
                complete=complete,
                meeting_id='0000000',
                moderator_passcode=settings.MODERATOR_PASSCODE,
                attendee_passcode=True,
                bitly_link_instructer=True,
                bitly_link_student_mobile=True,
                end_date_time=end_date_time,
                batch_type=batch_type,
                language_type=language_type
            )


            enrolled_course_ids = [Courses.objects.get(id=int(cid)).id for cid in courses_id_list]
            create_batch.courses.set(enrolled_course_ids)

            enrolled_student_ids = []
            for candidate_id in candidate_data:
                enroll_student = Enrollments.objects.get(id=int(candidate_id))
                enroll_student.batch = create_batch.id
                enroll_student.save()
                enrolled_student_ids.append(enroll_student.id)

            create_batch.enroll_student.set(enrolled_student_ids)


        send_batch_invite_email(request, Courses.objects.get(id=int(courses_id_list[0])).name, start_date_time, True, enrolled_student_ids)
        log_activity(request, action=choices.Action.add_batch, action_detail=choices.ActionDetails.add_batch, id=create_batch.id)

        room_emails = [enrollment.enquiry_course_id.enquiry_id.email for enrollment in Enrollments.objects.filter(id__in=candidate_data)]
        room_emails.append(Instructors.objects.get(id=int(instructors)).email)
        room_data = create_room_api(request, room_emails)

        if room_data.get('room_id'):
            Batches.objects.filter(id=create_batch.id).update(chat_room_id=room_data['room_id'])

        return redirect(reverse('batchlist'))

    context_data = {
        'instructor': Instructors.objects.filter(active=True),
        'enrollment': Enrollments.objects.all(),
        'course': Courses.objects.all().order_by('name'),
        'mindate': datetime.now().strftime('%Y-%m-%d')
    }
    return render(request, 'batches/batches_form.html', context_data)
@login_required(login_url = '/')
@custome_check()
def batchlist(request):
    batches = Batches.objects.all().order_by('-start_date_time')
    data = request.GET.copy()
    
    q_courses=request.GET.getlist('course')
    data['course'] = ','.join(q_courses)
    
    q_users=request.GET.getlist('user')
    data['user'] = ','.join(q_users)
    

    batches = BatchesFilter(data, batches).qs

    complete_batch=request.GET.get('complete_batch',None)
    active = False
    if complete_batch:
        batches = batches.filter(complete = True)
        active = True


    paginator = Paginator(batches, 10)
    page_number = request.GET.get('page')
    try:
        batches = paginator.page(page_number)
    except:
        batches = paginator.page(1)

    context_data = {
        'batches': batches,
        'users': Instructors.objects.all(),
        'courses': Courses.objects.all().order_by('name'),
        'q_courses': list(map(int, q_courses)),
        'q_users': list(map(int, q_users))
    
    }
    if active:
        context_data['active'] = 1
    return render(request, 'batches/list.html', context_data)

@login_required(login_url = '/')
@custome_check()
def batchView(request, batches_id):
    batches = Batches.objects.get(id=batches_id)
    batch_session_off = BatchSessionOff.objects.filter(batch=batches_id)
    instructors = Instructors.objects.all()
    data = []
    value = ""
    text_value = []
    context_data = {
        'batches': batches,
        'instructors': instructors,
        "text_value": value,
        'dows': anquira_handlers.DayOfWeekChoices.choice,
        'course': Courses.objects.all().order_by('name'),
        'batch_session_off':batch_session_off,
    }
    return render(request, 'batches/batches_view.html', context_data)

class BatchupdateView(View):
    redirect_url = "batchlist"

    def post(self, request, *args, **kwargs):
        # print("in post request of batch update "*1000)

        candidate_data = request.POST.get('candidate').split(',')
        days_of_week = ",".join(request.POST.getlist('days_of_week'))
        start_date_time = request.POST.get('start_date_time')
        session_duration = request.POST.get('session_duration')
        instructors = request.POST.get('instructors')
        try:
            complete = request.POST.get('complete')
        except:
            complete = 'False'
        courses_obj_id = Courses.objects.filter(id=int(request.POST['course']))
        print("courses_obj_id: ",courses_obj_id)
        courses_id=None
        if courses_obj_id.exists():
            print("yes exists")
            courses_id = courses_obj_id.first().id
        courses_obj_duration = Courses.objects.filter(id=int(courses_id))
        if courses_obj_duration.exists():
            duration = courses_obj_duration.first().duration
        candidate = ""
        candidate_extend_list = []
        for candidate_details in candidate_data:
            if candidate_details != "":
                candidate_extend_list.append(
                    Enrollments.objects.get(
                        id=int(candidate_details)
                    ).enquiry_course_id.enquiry_id.full_name
                )
        candidate = ", ".join(candidate_extend_list)
        batch_obj_instance = Batches.objects.filter(
            id=self.kwargs.get('batch_id')
        )
        if batch_obj_instance.exists():
            batch_obj_instance.update(
                days_of_week=days_of_week,
                instructors_id=int(instructors),
                session_duration=session_duration,
                candidates=candidate,
                complete=complete
            )
            for i in candidate_data:
                if i != "":
                    enroll_students = Enrollments.objects.get(id=int(i))
                    enroll_students.batch_id = batch_obj_instance.first().id
                    enroll_students.save()
                
                    enquiry = enroll_students.enquiry_course_id.enquiry_id 
                    email = enquiry.email
                    mobile = enquiry.mobile

                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={
                            'first_name': enquiry.full_name.split()[0] if enquiry.full_name else '',
                            'last_name': ' '.join(enquiry.full_name.split()[1:]) if len(enquiry.full_name.split()) > 1 else '',
                            'mobile': enquiry.mobile,
                            'user_type': 'student',
                            'is_active': True
                        }
                    )
                    user.set_password(str(email)+str(mobile))
                    user.save()
                    if created:
                        print(f"New user created: {user.email}")
                        send_batch_invite_email(request, Courses.objects.get(id=int(courses_id)).name, batch_obj_instance.first().start_date_time, True, enroll_students.id)    
        response_data = {
            'status': 1,
            'redirect': reverse(self.redirect_url)
        }

        try:
            log_activity(request,action=choices.Action.mod_batch, action_detail=choices.ActionDetails.mod_batch,id=self.kwargs.get('batch_id'))
        except Exception as e:
            print(e)
        return JsonResponse(response_data)


def get_filter_student(request):
    results = []
    s_string = request.GET['search_string']
    course_id= request.GET['course']
    enroll_find = request.GET.get("enroll_find",None)
    if enroll_find =="0":
        if s_string and course_id:
            if s_string != "":
                if s_string[0] in "0123456789":
                    e_objs = Enrollments.objects.filter(enquiry_course_id__enquiry_id__mobile__istartswith = s_string, enquiry_course_id__courses__id = int(course_id))
                    for e_obj in e_objs:
                        text = "{}). {} ({})".format(e_obj.id,e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile)
                        value = e_obj.id
                        results.append({"text": text, "value": value})
                else:
                    e_objs = Enrollments.objects.filter(enquiry_course_id__enquiry_id__full_name__istartswith = s_string, enquiry_course_id__courses__id = int(course_id))
                    for e_obj in e_objs:
                        text = "{}). {} ({})".format(e_obj.id,e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile)
                        value = e_obj.id
                        results.append({"text": text, "value": value})
    elif enroll_find=='1':
        if s_string and course_id:
            if s_string != "":
                if s_string[0] in "0123456789":
                    e_objs = Enrollments.objects.filter(id=int(s_string))
                    # e_objs = Enrollments.objects.filter(id=int(s_string), enquiry_course_id__courses__id = int(course_id))
                    for e_obj in e_objs:
                        text = "{}). {} ({})".format(e_obj.id,e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile)
                        value = e_obj.id
                        results.append({"text": text, "value": value})
    return render(request, 'batches/filtered_student.html',{'results':results})

def get_course_student(request):
    from datetime import datetime
    results = []
    course_id= request.GET.getlist('course',None)
    print(course_id)
    course_id = course_id[0]
    course_id = course_id.split(",")
    course_list = []
    for i in course_id:
        course_list.append(int(i))

    if course_id:
        temp_enroll_list = []
        later_date = datetime.now() - timedelta(days=100)
        later_enroll = Enrollments.objects.filter(added_on__gte = later_date)

        for le in later_enroll:
            enroll_course_data = le.enroll_courses
            enroll_course_data = enroll_course_data.split(",")
            for ecd in enroll_course_data:
                temp_enquiry_course_obj = EnquiryCourses.objects.filter(id=ecd).first()
                if temp_enquiry_course_obj.courses_id in course_list:
                    temp_enroll_list.append(le.id)



        if course_list:
            e_objs = Enrollments.objects.filter(id__in = temp_enroll_list).distinct().order_by('-id')
            for e_obj in e_objs:
                enroll_course = e_obj.enroll_courses
                if enroll_course:
                    enroll_course = enroll_course.split(",")
                    print(enroll_course)
                    course_list = []
                    for i in enroll_course:
                        try:
                            course_obj = EnquiryCourses.objects.filter(id=int(i)).first().courses.name
                        except Exception as e:
                            print(e)
                        course_list.append(course_obj)
                    print(course_list)
                text = "{}). {} ({}/{})--{}".format(e_obj.id,e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile,e_obj.enquiry_course_id.enquiry_id.email,course_list)
                value = e_obj.id
                results.append({"text": text, "value": value})
    return render(request, 'batches/filtered_student.html',{'results':results})


def get_student_name(request):
    id = request.GET.get('id',None)
    if id:
        stud_name = Enrollments.objects.filter(id=id).first()
        student_name = stud_name.enquiry_course_id.enquiry_id.full_name
        return JsonResponse({'student_name':student_name})

def removeStudentFromBatch(request):
    data={}
    enroll_id = request.GET.get('id',None)
    batch_id = request.GET.get('batch_id',None)
    if enroll_id:
        batch_obj = Batches.objects.filter(id=batch_id).first()
        batch_obj.enroll_student.remove(enroll_id)

        enroll_students = Enrollments.objects.get(id = int(enroll_id))
        student_email = enroll_students.enquiry_course_id.enquiry_id.email

        batch_obj = Batches.objects.filter(id=batch_id).first()

        user_obj =  User.objects.filter(email= student_email).last()
        try:
            if user_obj:
                room_id = batch_obj.chat_room_id
                print("Room Id  : ", room_id)
                room_obj = Room.objects.filter(id=room_id).first()
                room_obj.members.remove(user_obj.id)
        except Exception as e:
            print(e)


        return JsonResponse(data)

def update_batch(request):
    print("in post request of update_batch "*1000)

    batch_id = request.POST.get("batch_id",None)
    import datetime
    if batch_id:        
        courses_id_list = request.POST.getlist('course')

        candidate_data = request.POST['candidate2'].split(',') 
        
        if candidate_data[-1]=="":
            candidate_data.pop()
        candidate_data = list(dict.fromkeys(candidate_data))
        print("Candidate Data : ",candidate_data)
        days_of_week = ",".join(request.POST.getlist('days_of_week'))
        instructors = request.POST['instructors']
        session_duration = request.POST['session_duration']
        complete = request.POST.get('complete',False)
        batch_type = request.POST.get('batch_type')
        update_on = datetime.datetime.now()

        batch_status = request.POST.get("batch_status",None)
        print("batch_status: ",batch_status)
        print("days_of_week: ",days_of_week)
        print("instructors: ",instructors)
        print("session_duration: ",session_duration)
        print("complete: ",complete)
        print("batch_type: ",batch_type)
        if not batch_status:
            batch_status = "4"
        
        batch_obj = Batches.objects.filter(id=batch_id).first()

        if days_of_week:
            batch_obj.days_of_week = days_of_week
        if instructors:
            batch_obj.instructors = Instructors.objects.filter(id = instructors).first()
        if session_duration:
            batch_obj.session_duration = session_duration
        if complete:
            batch_obj.complete = complete
        if batch_type:
            batch_obj.batch_type = batch_type
        if update_on:
            batch_obj.updated_on = update_on
        batch_obj.batch_status = batch_status
        batch_obj.save()

        enroll_course_list = []
        for j in courses_id_list:
            enroll_course = Courses.objects.get(id = int(j))
            enroll_course_list.append(enroll_course.id)
        batch_obj.courses.set(enroll_course_list)
        
        for i in candidate_data:
            enroll_students = Enrollments.objects.get(id = int(i))
            batch_obj.enroll_student.add(enroll_students.id)
            student_email = enroll_students.enquiry_course_id.enquiry_id.email
            enquiry=Enquiries.objects.get(id=enroll_students.enquiry_course_id.enquiry_id.id)
            user_obj =  User.objects.filter(email= student_email).last()
            print("enroll_students id: ",enroll_students.id)
            if user_obj:
                room_id = batch_obj.chat_room_id
                room_obj = Room.objects.filter(id=room_id).first()
                room_obj.members.add(user_obj.id)
            else:
                user, created = User.objects.get_or_create(
                        email=student_email,
                        defaults={
                            'first_name': enquiry.full_name.split()[0] if enquiry.full_name else '',
                            'last_name': ' '.join(enquiry.full_name.split()[1:]) if len(enquiry.full_name.split()) > 1 else '',
                            'mobile': enquiry.mobile,
                            'user_type': 'student',
                            'is_active': True
                        }
                    )
                user.set_password(str(enquiry.email)+str(enquiry.mobile))
                user.save()
                if created:
                    print(f"New user created: {user.email}")
                    send_batch_invite_email(request, Courses.objects.get(id=int(enroll_course_list[0])).name, batch_obj.start_date_time, True, [enroll_students.id])  



    return redirect("/batches/view/"+str(batch_id)+"/")

def get_batch_recording(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
    ctx['batch_id']=batch_id
    if batch_id:
        demo_batch = Batches.objects.filter(id=batch_id).first()

        composite_list = get_recording_compositeContentId(request,demo_batch.meeting_id,demo_batch.instructors.blue_jeans_user_id)
        recording,total_minute = get_courses_recordings(request,composite_list,demo_batch.instructors.blue_jeans_user_id)
        ctx['recording']=recording
        ctx['base_url'] = settings.BASE_URL
    return render(request,"batches/batch_recording_list.html",ctx)

def weeknum(dayname):
	if dayname == 'Monday':   return 0
	if dayname == 'Tuesday':  return 1
	if dayname == 'Wednesday':return 2
	if dayname == 'Thursday': return 3
	if dayname == 'Friday':   return 4
	if dayname == 'Saturday': return 5
	if dayname == 'Sunday':   return 6

@login_required(login_url = '/')
@custome_check()
def batch_calender(request):
    from datetime import timedelta
    import datetime
    ctx={}

    instructore_id = request.GET.get("instructore",None)

    if instructore_id:
        all_batch_obj = Batches.objects.filter(instructors=instructore_id,batch_status=4)
    else:
        all_batch_obj = Batches.objects.all()
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
                batch_date_dict['title'] = str(i.id)+"- "+str("(")+i.instructors.name +str(") ")+ " and ".join(course_list)
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

    if instructore_id:
        demo_obj = Demo.objects.filter(instructors=instructore_id)
    else:
        demo_obj = Demo.objects.all()
    for demo in demo_obj:
        demo_dict = {}
        demo_dict['title']=str(demo.id)+"- "+str("(")+demo.instructors.name +str(") ")+"demo for "+ demo.courses.name
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
    user_instructor_obj = Instructors.objects.all()
    ctx['user_instructor']=user_instructor_obj
    ctx['instructore']=None
    if instructore_id:
        ctx['instructore']=instructore_id

    return render(request,"batches/batch_calender.html",ctx)


# Get recording for the Anquira batch listing not for classroom students and instructors..........

@csrf_exempt
def get_recording_for_anquira(request):
    ctx={}
    import datetime
    meeting_id = request.POST.get("meeting_id",None)

    batch_obj = Batches.objects.filter(id = meeting_id).first()

    # composite_list = get_recording_compositeContentId(request,meeting_id,batch_obj.instructors.blue_jeans_user_id)

    # recording,total_minute = get_courses_recordings(request,composite_list,batch_obj.instructors.blue_jeans_user_id)

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
    
    for f in l:
        re_obj = re.search(".*_((\d{8})\d{6})_.*", f)
        if re_obj:
            recorded_on = re_obj.group(1)
            l_dict[recorded_on] = f

    sorted_by_date = [l_dict[r] for r in sorted(l_dict.keys())]

    split_by_date = OrderedDict()

    for r in sorted_by_date:
        re_obj = re.search(".*_((\d{8})\d{6})_.*", r)
        if re_obj:
            recorded_on = re_obj.group(2)
            if  recorded_on in split_by_date:
                split_by_date[recorded_on].append(r)
            else:
                split_by_date[recorded_on] = []
                split_by_date[recorded_on].append(r)

    ctx['recording']=split_by_date

    batch_obj = Batches.objects.filter(meeting_id=meeting_id).last()
    ctx['batch_obj']=batch_obj

    recording_count = len(recording)
    ctx['recording_count']=recording_count

    ctx['total_minute'] =25

    # return render(request,'classroom/classroom_recordings.html',ctx)

    print(ctx)
    ctx['base_url'] = settings.BASE_URL
    return render(request,"batches/batch_recording_list.html",ctx)

def mark_recording(request):
    data={}
    reco_link = request.POST.get("reco_link",None)
    batch_type = request.POST.get("type",None)
    if reco_link:
        print(reco_link)
        batch_id = reco_link.split("@")
        batch_id = batch_id[1]
        if int(batch_type) == 1:
            batch_obj = Batches.objects.filter(id = batch_id).first()
            if batch_obj:
                course_list = []
                for j in batch_obj.courses.all():
                    course_list.append(j.name)
                course_name =  " and ".join(course_list)
        else:
            demo_batch_obj = Demo.objects.filter(id=batch_id).first()
            course_name = demo_batch_obj.courses.name
        
        # reco_link = reco_link.replace("class_recording","class_recording_demo")
        reco_link = reco_link.replace("class_recording","playback")

        if not BestRecording.objects.filter(link = reco_link).exists():
            x  = BestRecording(
                user_id = request.user.id,
                type = batch_type,
                link = reco_link,
                batch_demo_id = batch_id,
                batch_name = course_name
            )
            x.save()
    return JsonResponse(data)


@login_required(login_url = '/')
@custome_check()
def marked_recording(request):
    ctx={}
    best_recording_obj  = BestRecording.objects.all().order_by("-id")

    paginator = Paginator(best_recording_obj, 10)
    page_number = request.GET.get('page')
    try:
        best_recording_obj = paginator.page(page_number)
    except:
        best_recording_obj = paginator.page(1)

    ctx['best_recording_obj'] = best_recording_obj
    return render(request,'batches/marked_recording.html',ctx)


@login_required(login_url = '/')
@custome_check()
def removeMarkedRecording(request):
    data = {}
    id = request.GET.get("id",None)
    if id:
        BestRecording.objects.filter(id=id).delete()
    return JsonResponse(data)

@login_required(login_url = '/')
def get_batch_attendance(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
  
    if batch_id:
        batch_obj = Batches.objects.filter(id=batch_id).first()
        student_attendance = batch_obj.student_attendance
        if student_attendance:
            json_acceptable_string = student_attendance.replace("'", "\"")
            student_attendance = json.loads(json_acceptable_string)

            ctx['student_attendance']=student_attendance
    return render(request,"batches/batch_attendance.html",ctx)


def add_batch_session_off_date(request):
    if request.method =="POST":
        batch_id = request.POST.get("batchId",None)
        date_off = request.POST.get("addDateOff",None)
        
        if batch_id and date_off:
            if not BatchSessionOff.objects.filter(batch_id=int(batch_id),off_date = date_off).exists():
                x = BatchSessionOff(
                    batch_id = int(batch_id),
                    off_date = date_off
                )
                x.save()

                print("Sending Email to Student....")
                send_batch_off_reminder(batch_id,str(date_off))
        return redirect("/batches/view/"+str(batch_id)+"/")
    else:
        return redirect("/batches/list/")
    
def batch_progress(request):
    ctx={}
    batch_obj = Batches.objects.all().order_by("-id")

    print(batch_obj)
    print(len(batch_obj))

    paginator = Paginator(batch_obj, 10)
    page_number = request.GET.get('page')
    try:
        batch_obj = paginator.page(page_number)
    except:
        batch_obj = paginator.page(1)
        page_number = 1
        
    
    ctx['batch_obj']=batch_obj
    ctx['page_number']=page_number
    return render(request,'batches/batches_progres_list.html',ctx)

def get_batch_progress_data(request):
    ctx={}
    batch_obj = Batches.objects.all().order_by("-id")

    # print(batch_obj)
    # print(len(batch_obj))

    paginator = Paginator(batch_obj, 10)
    page_number = request.GET.get('page')
    try:
        batch_obj = paginator.page(page_number)
    except:
        batch_obj = paginator.page(1)

    ctx['batch_obj']=batch_obj
    # import time
    # time.sleep(5)


    batch_pro_data = []
    for i in batch_obj:
        temp_batch_data = {}
        all_batch_date = []
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
                all_batch_date.append(d)
        total_batch_days = len(all_batch_date)
        # print(total_batch_days)


        ACCESS_KEY = settings.ACCESS_KEY
        SECRET_KEY = settings.AWS_SECRET_KEY
        BUCKETNAME = settings.BUCKETNAME

        bucket = BUCKETNAME
        folder = "batch"+str("/")+str(i.id)+str("/")
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
        for f in l:
            re_obj = re.search(".*_((\d{8})\d{6})_.*", f)
            if re_obj:
                recorded_on = re_obj.group(1)
                l_dict[recorded_on] = f

        sorted_by_date = [l_dict[r] for r in sorted(l_dict.keys())]

        # print(sorted_by_date)
        split_by_date = OrderedDict()

        for r in sorted_by_date:
            re_obj = re.search(".*_((\d{8})\d{6})_.*", r)
            if re_obj:
                recorded_on = re_obj.group(2)
                if  recorded_on in split_by_date:
                    split_by_date[recorded_on].append(r)
                else:
                    split_by_date[recorded_on] = []
                    split_by_date[recorded_on].append(r)

        attended_class = list(split_by_date.keys())
        attended_class = len(attended_class)
        # print(attended_class)
        

        temp_batch_data['id'] = i.id
        temp_batch_data['name'] = i.batch_name
        temp_batch_data['days_of_week'] = i.days_of_week
        temp_batch_data['instructors_name'] = i.instructors.full_name
        temp_batch_data['start_date_time'] = i.start_date_time
        temp_batch_data['end_date_time'] = i.end_date_time
        temp_batch_data['total_class'] = total_batch_days
        temp_batch_data['attended'] = attended_class
        if not int(attended_class) == 0:
            persentage = (int(attended_class)*100)/int(total_batch_days)
        else:
            persentage = 0
        temp_batch_data['persentage'] = int(persentage)

        batch_pro_data.append(temp_batch_data)


    ctx['batch_pro_data']=batch_pro_data
    return render(request,'batches/batches_progres_table.html',ctx)


def batch_public_holiday(request):
    ctx={}
    batch_public_holiday_obj = PublicHoliday.objects.all()


    paginator = Paginator(batch_public_holiday_obj, 10)
    page_number = request.GET.get('page')
    try:
        batch_public_holiday_obj = paginator.page(page_number)
    except:
        batch_public_holiday_obj = paginator.page(1)
    
    ctx['batch_public_holiday_obj'] = batch_public_holiday_obj


    return render(request,'batches/batches_public_holiday.html',ctx)

def add_batch_public_holiday(request):
    if request.method == "POST":
        holiday_date = request.POST.get('holiday_date',None)
        ocassion = request.POST.get('ocassion',None)
        if holiday_date and ocassion:
            x = PublicHoliday(
                off_date = holiday_date,
                occasion = ocassion
            )
            x.save()

            sending_holiday_email(holiday_date,ocassion)
    return redirect(batch_public_holiday)


@csrf_exempt
def add_zoom_weebhook_response(request):
    data={}
    from datetime import datetime
    print("------------WeebHook-------------")

    print(request.body)
    bod= request.body
    if bod:
        import json
        bod = json.loads(bod)

    # headers = request.headers
    # print(headers)
    # print(type(headers))

    # a = {
    #         "applicationId": "_X0yuU3MSyyoVRkLHnAyaA",
    #         "monitorTime": 1653788650703,
    #         "traceId": "v=2.0;clid=aw1;rid=WEB_0dd7c95af0b2ba1af2463d0ca2fcef67",
    #         "accountId": "euZ5Pn17QeqiOUBytEf33g",
    #         "event": "meeting.ended",
    #         "status": "403",
    #         "userId": "Y4pNG63GTCW80lvcK0Kx-A",
    #         "url": "https://anquira.ap2v.com/batches/add-zoom-weebhook-response",
    #         "subscriptionId": "ZynZWIvISnapUVwpcN29WA",
    #         "requestHeaders": "N/A",
    #         "requestBody": {
    #             "event": "meeting.ended",
    #             "payload": {
    #                 "account_id": "euZ5Pn17QeqiOUBytEf33g",
    #                 "object": {
    #                     "duration": 60,
    #                     "start_time": "2022-05-29T01:42:20Z",
    #                     "timezone": "Asia/Calcutta",
    #                     "end_time": "2022-05-29T01:44:10Z",
    #                     "topic": "Test Meeting",
    #                     "id": "95162953252",
    #                     "type": 3,
    #                     "uuid": "aDg5N//rQuGfu/dPV5muqg==",
    #                     "host_id": "Y4pNG63GTCW80lvcK0Kx-A"
    #                 }
    #             },
    #         "event_ts": 1653788650463
    #         },
    #         "responseHeaders": {
    #             "Server": "nginx",
    #             "Content-Length": "1718",
    #             "Date": "Sun, 29 May 2022 01:44:11 GMT",
    #             "Content-Type": "text/html"
    #         }
    #     }

    meeting_id = bod['payload']['object']['id']
    events = bod['event']

    if events == "meeting.ended":
        batch_obj = Batches.objects.filter(zoom_meeting_id = meeting_id).last()
        if batch_obj:
            inst_email = batch_obj.instructors.email

            # inst_email = "neeraj@goognu.com"
            # res = remove_license_to_user(inst_email)
            # inc_meeting_license_number()

            ZoomMeetingIdUserBatch.objects.filter(meeting_id = batch_obj.zoom_meeting_id).update(
                meeting_status = 2,
                meeting_end_at = datetime.now()
            )

        if batch_obj:
            Batches.objects.filter(id = batch_obj.id).update(
                zoom_meeting_id = None,
                zoom_meeting_password = None,
                zoom_bitly_link_instructer = None,
                zoom_bitly_link_student_mobile = None,
                zoom_response_logs = None,
            )

    x = ZoomWeebHookResponce(
        response = request.body,
        response_type_log = bod
    )
    x.save()

    return HttpResponse("Webhook received!")


def get_end_date(request):
    print(request)
    course=request.GET.get('selectCourse',None)
    startDate=request.GET.get('startDate',None)
    days=request.GET.get('days',None)
    session_duration=request.GET.get('session_duration',None)
    courses=course
    course_list=courses.split(',')
    cd=0
    for i in course_list:
        course_duratioin = Courses.objects.filter(id = int(i)).first().duration
        cd+=course_duratioin
    # print(cd,'this is the duration')
    days=days
    count_d=days.split(',')
    count_day=len(count_d)
    duration = cd 
    s=startDate
    # start_date=s.split(' ')[0]
    starting_date=datetime.datetime.strptime(s, '%m/%d/%Y %I:%M %p')
    print(starting_date)
    daily_duration=int(session_duration)/60
    h_days=duration//daily_duration
    weeks=h_days//count_day
    endate=starting_date + timedelta(weeks=weeks)
    endate=endate + timedelta(minutes=int(session_duration))
    ending_date=datetime.datetime.strftime(endate, '%m/%d/%Y %I:%M %p')
    return JsonResponse({'ending_date':ending_date})