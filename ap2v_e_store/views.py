
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import CourseStoreCart
from recording_sessions.models import Recorded_Courses_name
from batches.models import CompleteRecording
from ap2v_courses.models import Courses
from enquiries.models import Enquiries, EnquiryCourses
from enrolls.models import Enrollments
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def add_course_to_cart(request):
    data={}
    if request.method == "POST":
        print("POST")
        if request.user.is_authenticated:
            print("authenticated")
            estore_course_id = request.POST.get("ecourse",None)
            print(estore_course_id)
            print('-----100'*100)
            if estore_course_id:
                if not CourseStoreCart.objects.filter(user_id = request.user.id,course_id = int(estore_course_id)).last():
                    print("Not foud")
                    x = CourseStoreCart(
                        user_id = request.user.id,
                        course_id = int(estore_course_id)
                    )
                    x.save()
                    data['code']=1
                    data['msg'] = "Course Added to Cart."
    return JsonResponse(data,status=400)
@csrf_exempt
def add_choice_to_cart(request):
    data={}
    if request.method == "POST":
        print("POST")
        # if request.user.is_authenticated:
        #     print("authenticated")
        ecourseid = request.POST.get("ecourse",None)
        ecoursetype = request.POST.get("etype",None)
        language = request.POST.get("avlang",None)
        print('thihfso lald tye', language)
        print('thihfso lald tye', type(language))
        
        print(ecourseid)
        anq_c_id=Courses.objects.filter(id=ecourseid).last()                    
        
        eng_recording=CompleteRecording.objects.filter(course_id=anq_c_id.anquira_course.id).last()
        if eng_recording:
            if not CourseStoreCart.objects.filter(user_id = request.user.id,course_id = int(ecourseid),course_type=ecoursetype).last():
                print("Not foud")
                x = CourseStoreCart(
                    user_id = request.user.id,
                    course_id = int(ecourseid),
                    course_type=ecoursetype,
                    available_lang=language,
                    batch_course_id=eng_recording.batch.id
                )
                x.save()
                data['code']=1
                data['msg'] = "Course Added to Cart."
        else:
            if not CourseStoreCart.objects.filter(user_id = request.user.id,course_id = int(ecourseid),course_type=ecoursetype).last():
                print("Not foud")
                x = CourseStoreCart(
                    user_id = request.user.id,
                    course_id = int(ecourseid),
                    course_type=ecoursetype,
                    available_lang=language,
                )
                x.save()
                data['code']=1
                data['msg'] = "Course Added to Cart."
        enquire_obj= Enquiries.objects.filter(email=request.user.email).last()
        if enquire_obj:
            enquire_course_obj=EnquiryCourses.objects.filter(enquiry_id_id=enquire_obj.id, courses_id=anq_c_id.anquira_course.id).last()
            if enquire_course_obj:
                enroll_obj=Enrollments.objects.filter(enquiry_course_id_id=enquire_course_obj.id,course_type=ecoursetype).last()
                data['enroll']=ecoursetype
                if enroll_obj:
                    CourseStoreCart.objects.filter(user_id = request.user.id,course_id = int(ecourseid),course_type=ecoursetype).delete()
                    
    return JsonResponse(data,status=200)

@csrf_exempt
def get_user_cart_count(request):
    data={}
    if request.method == "POST":
        print("POST")
        if request.user.is_authenticated:
            x = CourseStoreCart.objects.filter(user_id = request.user.id).count()
            data['count'] = x
            data['code']=1
            return JsonResponse(data,status=200)
    data['count'] = 0
    return JsonResponse(data)

def show_hide_model(request):
    data={}
    if request.method == "POST":
        ecourseid = request.POST.get("courseid",None)
        print('this ap2v',ecourseid)
        apc=Courses.objects.filter(id=ecourseid)
        for i in apc:
            anq_id=i.anquira_course.id

        language_obj=CompleteRecording.objects.filter(course_id=anq_id).all()
        l_list=[]
        for z in language_obj:
            if z:
                l_type=z.batch.language_type
                l_list.append(l_type)
                print('this is the language id',l_list)
                print(i.recording_price)
                data['language_type']=l_list
                data['result']=1
                if i.recording_price==0:
                    data['price']=0
                else:
                  data['price']=i.recording_price  
            else:
                data['result']=0
    return JsonResponse(data)

def language_add_batch(request):
    if request.method == "POST":
        cid = request.POST.get("course_id",None)
        lang_type = request.POST.get("language_type",None)
        print('ralk'*100)
        print('this is cid',cid)
        print('this is cid',type(cid))
        print('this is course language',lang_type)
        print('this is course language',type(lang_type))
        rc=Courses.objects.filter(id=cid).last()
        print('this dfghuiu',rc)
        rcb =rc.anquira_course.id
        print('this i srec',rcb)
        lang_obj=CompleteRecording.objects.filter(course_id=rcb).all()
        print('this is lang_ob',lang_obj)
        for z in lang_obj:
            print('this lana2222')
            print('bajfjtbf',z.batch.id)
            print('bajfjtbf',type(z.batch.id))
            print('bajfjtbf typeeeee',z.batch.language_type)
            if z.batch.id and z.batch.language_type==lang_type:
                print('pfgfhj6666666')
                print('safjhkasf',request.user.name)
                x=CourseStoreCart.objects.get(user_id = request.user.id,course_id = int(cid),course_type='1')
                print("this is batch id ",z.batch.id )
                # print('hjkl',x.batch_course.batch.id)
                print(type(x))
                x.batch_course_id=z.batch.id
                print('hello',z.batch.id)
                x.save()
                # CourseStoreCart.objects.create(user_id = request.user.id,course_id = rcb ,course_type=1,batch_course=z.batch.id) 
                # x = CourseStoreCart(
                #     user_id = request.user.id,
                #     course_id = rcb,
                #     course_type=1,
                #     batch_course=z.batch.id
                    
                # )
            else:
                continue
                
            
    return HttpResponse('ok')