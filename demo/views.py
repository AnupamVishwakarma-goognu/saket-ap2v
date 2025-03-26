from urllib import request
from django.shortcuts import render,redirect
from courses.models import Courses 
from instructors.models import Instructors
from enquiries.models import Enquiries
from django.db.models import Q
from django.http import JsonResponse
from anquira_v2 import anquira_handlers, choices
from .models import Demo,DemoSMSTemplate,DemoSaveVideo
from datetime import datetime
from communication.views import SendSMS,send_demo_invite_email
from django.conf import settings
from bluejeans.views import scheduled_meeting,genrate_bitly_link
from django.core.paginator import Paginator
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings
# from ap2v_courses.models import Courses
import urllib
import requests
import shutil
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError
import os
# from moviepy.editor import VideoFileClip
import datetime
import re
from collections import OrderedDict
from classroom.models import BatchStudentFeedback
from anquira_v2.decorators import custome_check
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from bluejeans.zoom import get_user_details,dec_meeting_license_number,zoom_scheduled_meeting,assign_license_to_user
from batches.models import ZoomLicenseDetails,ZoomMeetingIdUserBatch


# Create your views here.


@login_required(login_url = '/')
@custome_check()
def demoList(request):
    ctx={}
    ctx['course'] = Courses.objects.all().order_by('name')
    ctx['instructor'] = Instructors.objects.filter(active=True)
    demo_batch = Demo.objects.filter(descard=False).order_by("-create_on")
    ctx['smstemplate'] = DemoSMSTemplate.objects.all()

    paginator = Paginator(demo_batch, 10)
    page_number = request.GET.get('page')
    try:
        demo_batch = paginator.page(page_number)
    except:
        demo_batch = paginator.page(1)
    
    ctx['demo_batch'] = demo_batch

    return render (request,'demo.html',ctx)

def get_enquiry_student(request):
    ctx={}
    string = request.GET.get("search_string",None)
    if string:
        enquiry_obj = Enquiries.objects.filter(Q(full_name__icontains=string) | Q(email__icontains=string) | Q(mobile__icontains=string))[:5]
        ctx['enquiry_obj']=enquiry_obj
        return render(request,'filtered_student.html',ctx)

def get_student_name(request):
    data={}
    id = request.GET.get("id",None)
    if id:
        enq_obj = Enquiries.objects.filter(id=id).first()
        enq_obj = enq_obj.full_name
        data['student_name']=enq_obj
    return JsonResponse(data)

def create_demo_batch(request):
    course = request.POST.get("course",None)
    template_id = DemoSMSTemplate.objects.all().last().id
    date =  request.POST.get("date",None)
    s_time =  request.POST.get("start_time",None)
    e_time =  request.POST.get("end_time",None)
    from datetime import datetime

    # s_date_time = request.POST.get("start_date_time",None)
    # start_date_time = datetime.strptime(s_date_time, '%m/%d/%Y %I:%M %p')

    # e_date_time = request.POST.get("end_date_time",None)
    # end_date_time = datetime.strptime(e_date_time, '%m/%d/%Y %I:%M %p')

    start_date_time = datetime.strptime(date + " "+s_time, "%Y-%m-%d %H:%M")
    end_date_time = datetime.strptime(date + " "+e_time, "%Y-%m-%d %H:%M")
    
    instructor = request.POST.get("instructors",None)
    students = request.POST['candidate2'].split(',')
    batch_name = "demoBatch-{autogen}".format(autogen = anquira_handlers.get_batch_name())

    if students[-1]=="":
        students.pop()
    candidate_data = list(dict.fromkeys(students))

    attendees_data = []
    for i in candidate_data:
        attendees_email={}
        enquiry_students = Enquiries.objects.get(id = int(i))
        email = enquiry_students.email
        attendees_email['email'] = email
        attendees_data.append(attendees_email)

    instructors_obj = Instructors.objects.filter(id = instructor).first()
    user_id = None

    '''
    moderator_passcode = settings.MODERATOR_PASSCODE
    if instructors_obj.blue_jeans_user_id:
        user_id = instructors_obj.blue_jeans_user_id
        moderator_passcode = instructors_obj.blue_jeans_passcode

    title = "Demo - {}".format(Courses.objects.get(id = course).name)
    meeting_id,attendees_passcode = scheduled_meeting(request,title=title,description=title,start=start_date_time,end=end_date_time,attendees_list=[],user_id = user_id)
    
    #------NOTe : Please enable next 2 line of code for local testing, and comment above 1 line ----------
    # meeting_id = 160254125
    # attendees_passcode = 2569
    # moderator_passcode = 8581
    #---------Local Testing code end -----------------------------------------
    student_meeting_link = "https://bluejeans.com/"+str(meeting_id)+"/"+str(attendees_passcode)+"/webrtc"
    instructor_meeting_link = "https://bluejeans.com/"+str(meeting_id)+"/"+str(moderator_passcode)

    student_meeting_link = genrate_bitly_link(request,student_meeting_link)
    instructor_meeting_link = genrate_bitly_link(request,instructor_meeting_link)
    '''


    stu_list = (','.join(candidate_data))
    x = Demo(
        batch_name = batch_name, instructors = Instructors.objects.filter(id=instructor).first(),
        start_date_time = start_date_time, end_date_time = end_date_time,
        courses = Courses.objects.filter(id=course).first(), candidates = stu_list,
        created_by=request.user
    )
    x.save()
    title = Courses.objects.get(id = course).name+" Demo Batch"
    

    # res = SendSMS.send_demo_batch_sms_fast2sms(request,title,start_date_time,student_meeting_link,candidate_data,template_id)

    # send_demo_invite_email(request,title,start_date_time,student_meeting_link,candidate_data)

    return redirect("demoList")

def get_batch_student(request):
    ctx={}
    batch_id = request.GET.get("batch_id",None)
    ctx['batch_id']=batch_id
    if batch_id:
        demo_batch = Demo.objects.filter(id=batch_id).first()
        ctx['demo_batch']=demo_batch
        student_list = demo_batch.candidates
        student_list = student_list.split(",")

        '''
        composite_list = get_recording_compositeContentId(request,demo_batch.meeting_id,demo_batch.instructors.blue_jeans_user_id)
        recording,total_minute = get_courses_recordings(request,composite_list,demo_batch.instructors.blue_jeans_user_id)
        print(composite_list)
        print(recording)

        ctx['recording']=recording
        '''

        meeting_id = demo_batch.meeting_id

        batch_obj = batch_id

        # composite_list = get_recording_compositeContentId(request,meeting_id,batch_obj.instructors.blue_jeans_user_id)

        # recording,total_minute = get_courses_recordings(request,composite_list,batch_obj.instructors.blue_jeans_user_id)

        ACCESS_KEY = settings.ACCESS_KEY
        SECRET_KEY = settings.AWS_SECRET_KEY
        BUCKETNAME = settings.BUCKETNAME

        bucket = BUCKETNAME
        folder = "demo"+str("/")+str(batch_obj)+str("/")
        print(folder)
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
            # re_obj = re.search(".*_((\d{8})\d{6})_.*", f)
            re_obj = re.search(r".*_((\d{8})\d{6})_.*", f)
            if re_obj:
                recorded_on = re_obj.group(1)
                l_dict[recorded_on] = f

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

        # batch_obj = Batches.objects.filter(meeting_id=meeting_id).last()
        # ctx['batch_obj']=batch_obj

        # recording_count = len(recording)
        # ctx['recording_count']=recording_count

        # ctx['total_minute'] =25

        # return render(request,'classroom/classroom_recordings.html',ctx)

        print(ctx)


        ctx['base_url'] = settings.BASE_URL

        batch_student_list = []
        for i in student_list:
            enq_stu = {}
            enq_obj = Enquiries.objects.filter(id=i).first()
            if enq_obj.full_name:
                enq_stu['name'] = enq_obj.full_name
            if enq_obj.email:
                enq_stu['email'] = enq_obj.email
            if enq_obj.mobile:
                enq_stu['mobile'] = enq_obj.mobile
            batch_student_list.append(enq_stu)
        
        ctx['batch_student_list']=batch_student_list
        ctx['base_url'] = settings.BASE_URL
    return render(request,"batch_student_list.html",ctx)

def get_smsTemplate(request):
    data={}
    template_id = request.GET.get("template_id",None)
    if template_id:
        template_text = DemoSMSTemplate.objects.filter(id=template_id).first().template_text
        data['template_text']=template_text
    return JsonResponse(data)

def delete_batch(request):
    data ={}
    batch_id = request.GET.get("id",None)
    if batch_id:
        Demo.objects.filter(id=batch_id).update(
            descard = True
        )
    return JsonResponse(data)

def add_more_student(request):
    batch_id = request.POST.get("add_more_student_batch_id",None)
    students = request.POST['candidate23'].split(',')

    if students[-1]=="":
        students.pop()
    candidate_data = list(dict.fromkeys(students))


    demo_obj = Demo.objects.filter(id=batch_id).first()
    template_id = DemoSMSTemplate.objects.all().last().id
    start_date_time = demo_obj.start_date_time
    student_meeting_link = demo_obj.bitly_link_student_mobile
    title = "Demo - {}".format(Courses.objects.get(id = demo_obj.courses_id).name)

    res = SendSMS.send_demo_batch_sms_fast2sms(request,title,start_date_time,student_meeting_link,candidate_data,template_id)
    send_demo_invite_email(request,title,start_date_time,student_meeting_link,candidate_data)

    old_list = demo_obj.candidates.split(",")  
    new_list = old_list+candidate_data
    new_list_2 = []

    for i in new_list:
        if i not in new_list_2:
            new_list_2.append(i)

    candidate_data = (','.join(new_list_2))

    Demo.objects.filter(id=batch_id).update(
        candidates = candidate_data
    )
    return redirect("demoList")


def student_waiting_page(request,uuid=None):
    ctx={}
    if uuid:
        demo_obj = Demo.objects.filter(uuid= uuid).last()
        if demo_obj:
            print(demo_obj)
            ctx['demo_obj'] = demo_obj
            ctx['uuid'] = uuid
        else:
            return render(request,'v4_home/error_course_not_found.html',status=404)
    return render(request,'demo/demo_student_waiting_page.html',ctx)

@csrf_exempt
def student_check_for_demo_start(request):
    data={}
    uuid = request.GET.get("uuid",None)
    if uuid:
        demo_obj = Demo.objects.filter(uuid= uuid).last()
        if demo_obj:
            zoom_meeting_id = demo_obj.zoom_meeting_id
            zoom_bitly_link_instructer = demo_obj.zoom_bitly_link_instructer
            zoom_bitly_link_student_mobile = demo_obj.zoom_bitly_link_student_mobile

            if zoom_meeting_id and zoom_bitly_link_instructer and zoom_bitly_link_student_mobile:
                data['zoom_meeting_id'] = zoom_meeting_id
                data['zoom_bitly_link_instructer'] = zoom_bitly_link_instructer
                data['zoom_bitly_link_student_mobile'] = zoom_bitly_link_student_mobile
                data['code']=1
            else:
                data['error'] = "Instructor is not started demo yet..."
                data['code']=0
    return JsonResponse(data)

def waiting_to_start_demo(request,uuid):
    ctx={}
    if uuid:
        demo_obj = Demo.objects.filter(uuid= uuid).last()
        if demo_obj:
            print(demo_obj)
            ctx['demo_obj'] = demo_obj
            ctx['uuid'] = uuid
        else:
            return render(request,'v4_home/error_course_not_found.html',status=404)
    return render(request,'demo/demo_inst_waiting_page.html',ctx)


@csrf_exempt
def create_demo_sesion_zoom_meeting_id(request):
    ctx={}
    uuid = request.GET.get("uuid",None)
    meeting_responce = None
    print(uuid)

    demo_obj = Demo.objects.filter(uuid=uuid).last()
    if uuid:
        email = demo_obj.instructors.email
        # email = "neeraj@goognu.com"
        #check the user licence type...
        status_code,response = get_user_details(email)
        print(response)
        print(status_code)
        if status_code == 200:
            user_type = response['type']

            #creating meeting because it already licensed...
            if user_type == 2:
                print("****NOTE: USER IS ALREDY LICENSED.... ")
                course_list = []
                
                batch_title = demo_obj.courses.name+" Demo"
                
                nowDateTime = datetime.datetime.now()

                dec_meeting_license_number()

                batch_start_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                print("Demo Start Datetime Zoom Format : ",batch_start_date_time)

                from datetime import timedelta
                batch_end_date_time = nowDateTime+timedelta(minutes=180)
                batch_end_date_time = nowDateTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                print("Batch end Datetime Zoom Format : ",batch_end_date_time)

                print("******NOTE: CREATING MEETING FOR USER WHO ALREADY LICENSED")
                meeting_responce,zoom_password_random = zoom_scheduled_meeting(request,title=batch_title,description=None,start=batch_start_date_time,end=batch_end_date_time,attendees_list=None,zoom_user_email = email)
                print("******NOTE: MEETING CREATING SUCCEFULLY....")
            #assign license to user
            elif user_type == 1:
                print("******NOTE: USER IS NOT LICENSED ..... ")

                print("GETTING LICENSED DETAILS>>>>")
                license_obj = ZoomLicenseDetails.objects.all().last()
                total_license = license_obj.total_license
                use_license = license_obj.use_license

                free_license = int(total_license) - int(use_license)
                if free_license > 0:
                    print(" LICENSE FREE IS AVL.....")
                    print("****** NOTE: ASSIGNING A LICENSE TO USER....")
                    responce = assign_license_to_user(email)

                    check_licence_response = get_user_details(email)

                    print(check_licence_response)

                    user_type = check_licence_response[1]['type']

                    if user_type == 2:
                        print("DEC LICENSE NUMBER....")
                        dec_meeting_license_number()
                        if responce == 204:
                            #creating meeting after adding license...
                            course_list = []
                            
                            batch_title = demo_obj.courses.name+" Demo"
                            
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

                instructor_meeting_link_bitly = genrate_bitly_link(request,zoom_inst_url)
                student_meeting_link_bitly = genrate_bitly_link(request,zoom_stu_url)

                Demo.objects.filter(uuid=uuid).update(
                    zoom_meeting_id = meeting_id,
                    zoom_meeting_password = zoom_password_random,
                    zoom_bitly_link_instructer = instructor_meeting_link_bitly,
                    zoom_bitly_link_student_mobile = student_meeting_link_bitly,
                    zoom_response_logs = meeting_responce
                )

                print("Demo Updated....")


                x = ZoomMeetingIdUserBatch(
                    meeting_type = "2",
                    demo_id = demo_obj.id,
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
    return None

def waiting_page_for_student(request,uuid):


    return redirect("demoList")

def demoVideo(request):
    from ap2v_courses.models import Courses
    print('P'*100)
    ctx={}
    course_name=Courses.objects.all()
    ctx['course_name']=course_name
    return render(request, 'demovideo.html', ctx)

@csrf_exempt
def  demoSave(request):
    from ap2v_courses.models import Courses
    print('0'*100)
    if request.method == 'POST':
        cname=request.POST.get('dcourse')
        vfname=request.FILES.get('vfilename')
        # print(cname)
        # print(vfname)
        cn_obj=Courses.objects.filter(id=cname)
        # for i in cn_obj:
        #     print(i.name)
        #     print('ogfghjk'*100)

        if DemoSaveVideo.objects.filter(course_name=cname).exists():
            demoobj = DemoSaveVideo.objects.get(course_name=cname)
            demoobj.video_uload.delete()
            DemoSaveVideo.objects.filter(course_name=cname).delete()
        DemoVideo=DemoSaveVideo.objects.create(
            course_name_id=cname,
            file_name=vfname,
            video_uload=vfname
            )
    # ACCESS_KEY = settings.ACCESS_KEY
    # SECRET_KEY = settings.SECRET_KEY
    # BUCKETNAME = settings.BUCKETNAME

    
    # # file_name=settings.TEMP_RECORDING_STORE+str(i.course_name)+str('_')+str(i.date)+'.mp4'
    # # retitle=str(title).replace(" ", "_")
    # # --------------- duration of video -------------
    # # clip = VideoFileClip(vfname)
    # # print('pokijhfc'*100)
    # # print( clip.duration )
    # # ----------------
    # date=datetime.datetime.now()
    # sdate=date.strftime("%Y%m%d%f")
    # s3_file_name = 'democlass/'+str(cname)+str('/')+str(i.name)+str('_')+str(sdate)+str('00.00')+'.mp4'

    # # from django.core.files.storage import default_storage
    # # file_name = default_storage.save(video.name, video)
    # from django.core.files.storage import FileSystemStorage
    # fs = FileSystemStorage(settings.DEFAULT_FILE_STORAGES) #defaults to   MEDIA_ROOT  
    # uploaded_file_name = str(vfname.name).replace(" ","_")
    # filename = fs.save(uploaded_file_name, vfname)
    # file_url = fs.url(filename)
    # print(file_url)
    # sfile_name = str(file_url)
    # sfile_name = sfile_name.replace("/media/","")

    # complete_file_name = settings.TEMP_RECORDING_STORE+sfile_name

    


    # local_file = complete_file_name
    # # local_file = video.NamedTemporaryFile()
    # print(local_file)
    # bucket = BUCKETNAME
    # s3_file = s3_file_name

    # s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    
    # # ---------------------------------update video----------------
    # folder='demo/'+str(cname)
    # prefolder='demo/'+str(cname)+str('/')
    # response = s3.list_objects_v2(Bucket=bucket, Prefix=prefolder)
    # if 'Contents' in response:
    #     files_in_folder = response["Contents"]
    #     files_to_delete = []
    #     # We will create Key array to pass to delete_objects function
    #     for f in files_in_folder:
    #         files_to_delete.append({"Key": f["Key"]})
    #     # This will delete all files in a folder
    #     response = s3.delete_objects(
    #         Bucket=bucket, Delete={"Objects": files_to_delete}
    #     )
    # try:
    #     s3.upload_file(local_file, bucket, s3_file)
    #     print("****Upload Successful-")
        

    #     try:
    #         os.remove(complete_file_name)
    #         print("file deleted")
    #     except Exception as e:
    #         print(e)
    # except FileNotFoundError:
    #     print("****The file was not found")
    # except NoCredentialsError:
    #     print("****Credentials not available")   
    return redirect("demoVideo")



    