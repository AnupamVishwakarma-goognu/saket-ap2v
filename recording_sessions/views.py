# from ctypes.wintypes import PINT
from http import client
from pydoc import cli
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse, JsonResponse
from ap2v_courses.models import Courses
from ap2v_e_store.models import CourseStoreCart
from enquiries.models import Enquiries,EnquiryCourses
from django.views.decorators.csrf import csrf_exempt
# from. models import Recorded_Courses_name,Recorded_Uploading_S3_Logs, Order,PaymentStatus,temp_order_detail
from . models import Recorded_Courses_name,Recorded_Uploading_S3_Logs,Order,temp_order_detail,PaymentStatus,OnlineBuyedCourse
from datetime import datetime, timedelta
from django.conf import settings
import os
from botocore.exceptions import NoCredentialsError
import boto3
import shutil
from moviepy import VideoFileClip
import razorpay
from enrolls.models import Enrollments
from users.models import CustomUserModel
from batches.models import CompleteRecording,Batches



# Create your views here.
def recordingclass(request):
    
    context_data = {   
        'course': Courses.objects.all().order_by('name'),
    }
    return render(request, 'sessions.html', context_data)

@csrf_exempt
def recordingVideo(request):
   
    print(request)
    if request.method == 'POST':
        print('we are using post method')
        course=request.POST.get('rcourse', None)
        video=request.FILES.get('vfilename', None)
        title=request.POST.get('title', None)
        print(video)
        print(type(video))
        rcn_obj=Recorded_Courses_name.objects.filter(course_id=course).last()
        if rcn_obj:
            Recorded_Courses_name.objects.filter(id=rcn_obj.id).update(number=int(rcn_obj.number)+1)
        else:
            rcn_obj=recordingVideo=Recorded_Courses_name.objects.create(course_id=course,status=True)
            
        
        if rcn_obj:
            recordingVideo=Recorded_Uploading_S3_Logs.objects.create(course_name_id=rcn_obj.id,name=video,date=datetime.now(),status=True)
        else:
            print('this is very easy')
        
    else:
        print('this is else part')


    print(video)
    print(type(video))
    try:
        clip = VideoFileClip(video)
        duration = int((clip.duration)/60)
        print("Duration of local is :", duration)
        # del clip
    except Exception as e:
        print(e)
    run_obj=Recorded_Uploading_S3_Logs.objects.all()
    for j in run_obj:
        date = str(j.date.strftime('%Y%m%d'))

    ACCESS_KEY = settings.ACCESS_KEY
    SECRET_KEY = settings.AWS_SECRET_KEY
    BUCKETNAME = settings.BUCKETNAME

    
    # file_name=settings.TEMP_RECORDING_STORE+str(i.course_name)+str('_')+str(i.date)+'.mp4'
    retitle=str(title).replace(" ", "_")
    s3_file_name = 'rsession/'+str('24')+str('/')+str(rcn_obj.number)+str('_')+str(retitle)+str('_')+str(course)+str('_')+str(date)+str('_')+str('00.00')+'.mp4'

    # from django.core.files.storage import default_storage
    # file_name = default_storage.save(video.name, video)
    from django.core.files.storage import FileSystemStorage
    fs = FileSystemStorage(settings.DEFAULT_FILE_STORAGE) #defaults to   MEDIA_ROOT  
    uploaded_file_name = str(video.name).replace(" ","_")
    filename = fs.save(uploaded_file_name, video)
    file_url = fs.url(filename)
    print(file_url)
    sfile_name = str(file_url)
    sfile_name = sfile_name.replace("/media/","")

    complete_file_name = settings.TEMP_RECORDING_STORE+sfile_name
    print(complete_file_name)
    print('jb'*100)

    


    local_file = complete_file_name
    # local_file = video.NamedTemporaryFile()
    print('ashi'*100)
    print(local_file)
    bucket = BUCKETNAME
    s3_file = s3_file_name
    print(s3_file_name)

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("****Upload Successful-")
        # Recorded_Uploading_S3_Logs.objects.filter(id=i.id).update(
        #     upload=True
        # )

        try:
            os.remove(complete_file_name)
            print("file deleted")
        except Exception as e:
            print(e)
    except FileNotFoundError:
        print("****The file was not found")
    except NoCredentialsError:
        print("****Credentials not available")

    return redirect("recordingclass")

    
# RAZORPAY_KEY = "rzp_test_WyFwGAjnFaTozW"
# RAZORPAY_SECERT = "Iqz6lVM5eKD6VLvOV0jVKGlU"
def cart_checkout_page(request):
    ctx={}
    user_id=request.user.id
    # user_nmae=request.user.name
    if request.method == 'POST':
        course=request.POST.get('courseid', None)
        price=request.POST.get('price', None)
        print('apapa'*100)
        print(course)
        
        if course:
            CourseStoreCart.objects.filter(id=course).delete()
    
        # print('man'*100)
        # print(user_id)
    course_select=CourseStoreCart.objects.filter(user_id=user_id)
    price=0
    item=0
    courselist=[]
    cartlist=[]
    
    for x in course_select:
        print(x.course_type)
        print(type(x.course_type))
        print('0'*100)
        if x.course_type == '1':
            mrp=x.course.recording_price
            print('this iis 1 type',mrp)
            price+=mrp
            item+=1
            c=x.course.id
            courselist.append(c)
            cartlist.append(x.id)
            user_name=x.user
            

            
            # for lg in ab_lang:
            #     lang_list=[]
            #     if lg.batch.language_type=='1':
            #         lang_list.append(1)
            #     elif: 
            #     else:
            #         lang_list.append(2)
            #     ctx['lang']=lang_list
            # print('this  i s language id', lang_list)
        else:
            mrp=x.course.price
            print('this iis 2 type',mrp)
            price+=mrp
            item+=1
            c=x.course.id
            courselist.append(c)
            cartlist.append(x.id)
            user_name=x.user
        

   
    # courselist=[]
    # cartlist=[]
    # for i in course_select:
    #     c=i.course.id
    #     courselist.append(c)
    #     cartlist.append(i.id)
    #     user_name=i.user
        # item+=1
        # price+=i.course.course.price
    print(courselist)
    print('<>'*100)
    order_currency="INR"
    ctx['item']=item
    ctx['price']=price
    # ctx['mrp']=mrp
    amount=price*100
    if amount>0:
        razorpay_client=razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECERT))
        payment_order=razorpay_client.order.create({'amount':amount, 'currency':order_currency,'payment_capture':'1'})
        order_id=payment_order['id']
        order=Order.objects.create(name=user_name,amount=mrp, provider_order_id=order_id)
        order.save()
        # order.courses.set(courselist)
        temp_order=temp_order_detail.objects.create(user_name=user_name, order_id=order_id)
        temp_order.save()
        # temp_order.course.set(courselist)
        # temp_order.cart.set(cartlist)



        callback_url = 'paymenthandler/'
        # print('this is user',user_name)
        ctx['course_select']=course_select
        ctx['user_name']=user_name
        ctx['callback_url'] = callback_url
        ctx['razorpay_order_id'] = order_id
        ctx['razorpay_merchant_key'] = settings.RAZORPAY_KEY
        ctx['order_currency']=order_currency
        ctx['amount']=amount
        return render(request,'course_detail_cart.html', ctx)
    else:
        return render(request,'not_add_item.html')

# @csrf_exempt
# def delete_item(request):
#     if request.method == 'POST':
#         print('we are using post method')
#         course=request.POST.get('courseid', None)
#         print('apapa'*100)
#         print(course)
#     return render(request,'course_detail_cart.html')



# @csrf_exempt
# def payment_recording_session(request):
#     p=request.GET.get('price',None)
#     price=p*100
#     oreder_currency="INR"
#     print(p)
#     print('thsi'*100)
#     client=razorpay.Client(auth=(RAZORPAY_KEY,RAZORPAY_SECERT))
#     payment=client.order.create({'amount':price, 'currency':oreder_currency,'payment_capture':'1'})
#     return render(request,'paymentSuccess.html')

@csrf_exempt
def paymenthandler(request):
    user_id=request.user.id
    user_email=request.user.email
    user_mobile=request.user.mobile
    user_name=request.user.name
    print('stay your dision'*100)
    print(user_id)
    print(user_name)
    print(user_mobile)
    print(user_email)
    razorpay_client=razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECERT))
    ctx={}
    if request.method == "POST":
        confirm_data = request.POST
        print("-----------------------------------------------------")
        print(confirm_data)
        order_id = confirm_data['razorpay_order_id']
        if confirm_data['razorpay_order_id'] and confirm_data['razorpay_payment_id'] and confirm_data['razorpay_signature']:
            order_details = Order.objects.filter(provider_order_id = order_id).first()
            order_details.provider_order_id = confirm_data['razorpay_order_id']
            order_details.payment_id = confirm_data['razorpay_payment_id']
            order_details.signature_id = confirm_data['razorpay_signature']
            # order_details.payment_status = True
            order_details.status = PaymentStatus.SUCCESS
            order_details.save()
            ctx['order_details'] = order_details
            course_select=CourseStoreCart.objects.filter(user_id=user_id).all()
            for i in course_select:
                c=i.course.id
                enq_c_id=i.course.anquira_course.id
                ctype=i.course_type
                if i.course_type == '1':
                    
                    rcb_id=i.batch_course.id
                    print('a',c)
                    print('b',ctype)
                    print('c',enq_c_id)
                    print('this is the  rcb id',rcb_id)
                    
                    buy_course=OnlineBuyedCourse.objects.create(user_id_id=user_id,order_id=order_details.id,course_id=c,course_type=ctype,batch_id_id=rcb_id)
                    buy_course.save()
                else:
                    buy_course=OnlineBuyedCourse.objects.create(user_id_id=user_id,order_id=order_details.id,course_id=c,course_type=ctype)
                    buy_course.save()
            # buy_course.course.set(courselist)

            temp_order_detail.objects.all().delete()
            CourseStoreCart.objects.filter(user_id=user_id).delete()
            # ------enq--------------------
                    
            # course = Courses.objects.all().order_by('name')
            # if request.method == 'POST':
                # courses = request.POST.getlist('course')
                # selectCourses = courses[0].split(',')
                # print('this is spliting'*100)
                # print(selectCourses)
            
            enq_onj=Enquiries.objects.filter(email=request.user.email).last()
            if enq_onj:

                buy_courses=OnlineBuyedCourse.objects.filter(user_id_id=user_id,).all()
                for obc in buy_courses:
                    obc_id=obc.course.anquira_course.id
                    print('this enquiry exits id ',obc_id)
                    print('type of course',type(obc.course_type))
                    # if obc_id:
                    if obc.course_type == '1':  
                            obc_id=obc.course.anquira_course.id
                            
                            enq_cou_obj=EnquiryCourses.objects.filter(enquiry_id_id = enq_onj.id, courses_id = obc_id).last()
                            if enq_cou_obj:
                                continue
                            else:
                            # else:
                            #     print("Course not found for course_id:",obc_id)
                                EnquiryCourses.objects.create(enquiry_id_id = enq_onj.id, courses_id = obc_id)
                                Enquiries.objects.filter(id = enq_onj.id).update()
                            
                            enq_cou_id=EnquiryCourses.objects.filter(enquiry_id_id=enq_onj.id).last()
                            # for enq_c_id in enq_cou_id:
                            enqc_ic=enq_cou_id.id
                            Enrollments.objects.create(enquiry_course_id_id=enq_cou_id.id,enroll_courses=enqc_ic,discussed_fee=obc.course.recording_price,payment_method_id=2,registered_by_id=settings.REGISTERED_BY,course_type= obc.course_type)
                            # complete_course=CompleteRecording.objects.filter(course_id=obc_id).last()
                            enroll_no=Enrollments.objects.filter(enquiry_course_id_id=enqc_ic).last()
                            add_batch=Batches.objects.filter(id=obc.batch_id.id).last()
                            add_batch.enroll_student.set([enroll_no.id])
                            add_batch.save()
                                
                    else:
                        obc_id=obc.course.anquira_course.id
                        enq_C_obj=EnquiryCourses.objects.filter(enquiry_id_id = enq_onj.id, courses_id = obc_id).last()
                        if enq_C_obj:
                            enrolls_objs=Enrollments.objects.filter(enquiry_course_id_id=enq_C_obj.id,enroll_courses=obc_id,).last()
                            if enrolls_objs:
                                continue
                            else:
                                Enrollments.objects.create(enquiry_course_id_id=enq_C_obj.id,enroll_courses=obc_id,discussed_fee=obc.course.price,payment_method_id=2,registered_by_id=settings.REGISTERED_BY,course_type=obc.course_type)
                        else:
                            EnquiryCourses.objects.create(enquiry_id_id = enq_onj.id, courses_id = obc_id)
                        # # else:
                        # #     print("Course not found for course_id:",obc_id)
                            Enquiries.objects.filter(id = enq_onj.id).update()
                        
                            enq_cou_id=EnquiryCourses.objects.filter(enquiry_id_id=enq_onj.id).last()
                        # for enq_c_id in enq_cou_id:
                            if enq_cou_id:
                                enqc_ic=enq_cou_id.id
                                enrolls_obj=Enrollments.objects.filter(enquiry_course_id_id=enq_cou_id.id,enroll_courses=enqc_ic,).last()
                                if enrolls_obj:
                                    continue
                                else:
                                    Enrollments.objects.create(enquiry_course_id_id=enq_cou_id.id,enroll_courses=enqc_ic,discussed_fee=obc.course.price,payment_method_id=2,registered_by_id=settings.REGISTERED_BY,course_type=obc.course_type)
            else:

                try:
                    print('1st step')
                    enq=Enquiries()
                    fullname=request.user.name
                    if fullname:
                        enq.full_name=fullname
                    
                    email=request.user.email
                    if email:
                        enq.email=email.lower()
                    
                    # mobile=request.POST.get('mobile',False)
                    # mobile = mobile.split("#")
                    mobile=request.user.mobile
                    print(mobile)
                    if mobile:
                        enq.mobile=mobile

                    assigned_by=settings.REGISTERED_BY
                    if assigned_by:
                        enq.assigned_by_id=assigned_by
                    
                    enq.save()
                    data =enq
                    # for course in selectCourses:
                    # coursedata_id = Courses.objects.filter(id = c).last()
                    print('2nd step')
                    buy_courses=OnlineBuyedCourse.objects.filter(user_id_id=user_id,).all()
                    for obc in buy_courses:
                        obc_id=obc.course.anquira_course.id
                        print('this obc id ',obc_id)
                        print('type of course',type(obc.course_type))
                        print('this is batch id', obc.batch_id)
                        # if obc_id:
                        if obc.course_type == '1':
                            obc_id=obc.course.anquira_course.id
                            
                            EnquiryCourses.objects.create(enquiry_id_id = data.id, courses_id = obc_id)
                            # else:
                            #     print("Course not found for course_id:",obc_id)
                            Enquiries.objects.filter(id = data.id).update()
                            
                            enq_cou_id=EnquiryCourses.objects.filter(enquiry_id_id=data.id).all()
                            print('3rd step')
                            for enq_c_id in enq_cou_id:
                                
                                print('thihs equire id',enq_c_id)
                                enqc_ic=enq_c_id.id
                                exit_enroll=Enrollments.objects.filter(enquiry_course_id_id=enq_c_id.id,enroll_courses=enqc_ic).last()
                                if exit_enroll:
                                    continue
                                else:
                                    Enrollments.objects.create(enquiry_course_id_id=enq_c_id.id,enroll_courses=enqc_ic,discussed_fee=obc.course.recording_price,payment_method_id=2,registered_by_id=settings.REGISTERED_BY,course_type=obc.course_type)
                                    print('3dddddd')
                                    # complete_course=CompleteRecording.objects.filter(course_id=obc_id).last()
                                    print('4th step')
                                    enroll_no=Enrollments.objects.filter(enquiry_course_id_id=enqc_ic).last()
                                    print('this enrollment id'*100)
                                    print(enroll_no.id)
                                    add_batch=Batches.objects.filter(id=obc.batch_id.id).last()
                                    add_batch.enroll_student.set([enroll_no.id])
                                    add_batch.save()
                                
                        else:
                            print('yaha pr pahuch gya h ')
                            obc_id=obc.course.anquira_course.id
                            enq_C_obj=EnquiryCourses.objects.filter(enquiry_id_id = data.id, courses_id = obc_id).last()
                            print('mk 2nd ')
                            if enq_C_obj:
                                print('ye if me h')
                                continue
                            else:
                                EnquiryCourses.objects.create(enquiry_id_id = data.id, courses_id = obc_id)
                                print('else me h')
                            # else:
                            #     print("Course not found for course_id:",obc_id)
                            Enquiries.objects.filter(id = data.id).update()
                            
                            enq_cou_id=EnquiryCourses.objects.filter(enquiry_id_id=data.id).last()
                            print('300rd step')
                            # for enq_c_id in enq_cou_id:
                                
                            print('thihs shivam equire id',enq_cou_id.id)
                            enqc_ic=enq_cou_id.id
                            print('thisef is stud ',enqc_ic)
                            exit_enroll=Enrollments.objects.filter(enquiry_course_id_id=enq_cou_id.id,enroll_courses=enqc_ic).last()
                            if exit_enroll:
                                continue
                            else:
                                Enrollments.objects.create(enquiry_course_id_id=enq_cou_id.id,enroll_courses=enqc_ic,discussed_fee=obc.course.price,payment_method_id=2,registered_by_id=settings.REGISTERED_BY,course_type=obc.course_type)
                            # print('3dddddd')
                            # # complete_course=CompleteRecording.objects.filter(course_id=obc_id).last()
                            # print('4th step')
                            # enroll_no=Enrollments.objects.filter(enquiry_course_id_id=enqc_ic).last()
                            # print('this enrollment id'*100)
                            # print(enroll_no.id)
                            # add_batch=Batches.objects.filter(id=complete_course.batch.id).last()
                            # add_batch.enroll_student.set([enroll_no.id])
                            # add_batch.save()

                    
                except Exception as e:
                    print(e)
                    print('this try'*10)
                    return JsonResponse({"result": False}, status=500)
                    all_users = CustomUserModel.objects.filter(is_staff=False, exist_employee=True)
            # ------enq--------------------
        return render(request, 'paymentSuccess.html',ctx)
    order_details.status = PaymentStatus.FAILURE
    order_details.save()
    temp_order_detail.objects.all().delete()
    return render(request, 'paymentfail.html',ctx)
    
    
            
       
def recordin_session_record(request):
    ctx={}
    order_obj=OnlineBuyedCourse.objects.all()
    ctx['order']=order_obj
    return render(request,'order_session_record.html',ctx)

