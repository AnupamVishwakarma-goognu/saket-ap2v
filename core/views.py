from django.shortcuts import render

from PIL import Image
import requests
import imagehash
import os
from django.conf import settings
from django.core.files.storage import default_storage,FileSystemStorage
import numpy as np
from .models import Image as ImageModel, AuthToken
from django.http import HttpResponse, JsonResponse
from communication.models import CounselorContactNumber
import uuid
from batches.models import Batches
from core.models import UrlCacheScriptLog
from django.core.paginator import Paginator

# Create your views here.

def check_duplicate_image(image):
    data = {}
    data['status'] = 1
    data['name'] = None
    if image:
        hash_size = 8
        with Image.open(image , 'r') as img:
            temp_hash = imagehash.average_hash(img, hash_size)

        img_obj = ImageModel.objects.filter(hash_value=temp_hash).first()

        if img_obj:
            data['status'] = 0
            data['name'] = img_obj.image
        else:
            x = ImageModel(
                image = image,
                hash_value = temp_hash
            )
            x.save()
            data['status'] = 1
            data['name'] = str(image)
    return data


def get_counselor_round_number(request):
    data = {}
    number = CounselorContactNumber.objects.filter(used_number=False).first()
    if number is None:
        all_number = CounselorContactNumber.objects.all()
        for i in all_number:
            CounselorContactNumber.objects.filter(id=i.id).update(
                used_number = False
            )
        number = CounselorContactNumber.objects.filter(used_number=False).first()
        if number:
            CounselorContactNumber.objects.filter(number=number.number).update(
                used_number = True
            )
        # return number.number
            data['number'] = number.number
        else:
            data['number']="0000000000"
        return JsonResponse(data)
    else:
        CounselorContactNumber.objects.filter(number=number.number).update(
            used_number = True
        )
        # return number.number
        data['number'] = number.number
        return JsonResponse(data)

def get_promotion_data(request_id):
    from promotions.models import Campaign
    request_obj = Campaign.objects.filter(id=request_id).first()
    return request_obj

def mark_complete_promotion_send_email_sms(request_id):
    from promotions.models import Campaign
    request_obj = Campaign.objects.filter(id=request_id).update(
        complate = True
    )
    return request_obj

def get_bulk_email_data(request_id):
    from promotions.models import SendBulkMail
    request_obj = SendBulkMail.objects.filter(id=request_id).first()
    return request_obj


def get_template(code):
    html_template = None
    if code == "OTE-01":
        html_template = "onlinetraning.html"
    return html_template

def save_bulk_email_data(id,emails_send_response):
    from promotions.models import SendBulkMail
    SendBulkMail.objects.filter(id=id).update(
        is_complete = True,
        json_result = emails_send_response 
    )
    return "1"







#Get IP Country Ip Location Code.
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_country_ip_loc(request):
    data={}
    ip = request.POST.get('ip',None)
    
    data['country_iso'] = ip
    return JsonResponse(data)




def validate_auth_token(request):
    data={}
    auth_token = request.GET.get('auth_token',None)
    print(auth_token)
    try:
        uuid.UUID(str(auth_token))
        
    except ValueError:
        data['message'] = "invalid requrest"
        return JsonResponse(data, status=400)

    if AuthToken.objects.filter(token = auth_token).exists():
        auth_token_obj = AuthToken.objects.filter(token = auth_token).first()
        name = auth_token_obj.user.first_name
        email = auth_token_obj.user.email
        data['name'] = name
        data['email'] = email

        batch_obj = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email =email)
        print(batch_obj)

        course_dict = {}
        for i in batch_obj:
            c = i.courses.all()
            print(c)
            for ic in c:
                print(ic.name)
                print(ic.id)
                course_dict[ic.id] = ic.name
        data['course'] = course_dict
        data['token'] = auth_token


        return JsonResponse(data, status=200)
    else:
        data['message'] = "invalid requrest"
        return JsonResponse(data, status=400)


def url_cache_script_logs(request):
    ctx={}
    logs_obj = UrlCacheScriptLog.objects.all().order_by("-id")
    

    paginator = Paginator(logs_obj, 10)
    page_number = request.GET.get('page')
    try:
        logs_obj = paginator.page(page_number)
    except:
        logs_obj = paginator.page(1)

    ctx['logs_obj']=logs_obj
    return render(request,'url_cache_log.html',ctx)