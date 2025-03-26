from urllib import response
from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from .models import AccessToken
import datetime
from django.conf import settings
import pytz
import jwt
import requests
import random
from batches.models import ZoomLicenseDetails

def zoom_scheduled_meeting(request,title=None,description=None,start=None,end=None,attendees_list=None,zoom_user_email = None):
    now = datetime.datetime.now()

    email = settings.ZOOM_ADMIN_EMAIL
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    amsterdam_timezone = pytz.timezone('Asia/Kolkata')
    date_search = amsterdam_timezone.localize(now)
    print("Now : ",date_search.date())


    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=5)
    round_off_datetme = round(experation_time.timestamp())
    headers = {"alg":"HS256", "typ":"JWT"}
    payload = {"iss":api_key,"exp":round_off_datetme}
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")

    # batch_start_date_time = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    # batch_end_date_time = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    zoom_password_random = random.randint(1000,9999)

    url = "https://api.zoom.us/v2/users/{}/meetings".format(zoom_user_email)
    obj = {"topic":title,"password":zoom_password_random,
            "settings":{"allow_multiple_devices":True,"auto_recording":"cloud","watermark":True},
            "type":1}
    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    create_meeting = requests.post(url,json=obj,headers=header)
   
    response = create_meeting.text
    # print(response)
    
    response_dict = json.loads(response)
    print(response_dict)

    # zoom_inst_url = response_dict['start_url']
    # zoom_stu_url = response_dict['join_url']

    # bitly_int_url = genrate_bitly_link(self,zoom_inst_url)
    # bitly_stu_url = genrate_bitly_link(self,zoom_stu_url)
    return response_dict,zoom_password_random

def create_zoom_user(name,email,password):
    data_dict = {}

    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    print(round_off_datetme)

    headers = {"alg":"HS256", "typ":"JWT"}
    payload = {"iss":api_key,"exp":round_off_datetme}
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")

    url = "https://api.zoom.us/v2/users"
    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    obj = {
            "action": "create",
            "user_info": {
                "last_name": "",
                "type": 1,
                "feature": {
                    "zoom_phone": False
                }
                }
            }
    obj['user_info']['email'] = email
    obj['user_info']['first_name'] = name 
    obj['user_info']['password'] = password

    print(obj)

    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    create_user = requests.post(url,json=obj,headers=header)

    print(create_user)
    print("**"*30)
    print(create_user.text)
    return create_user.text



def get_user_details(email):
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    print(round_off_datetme)

    headers = {"alg":"HS256", "typ":"JWT"}
    payload = {"iss":api_key,"exp":round_off_datetme}
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")



    url = "https://api.zoom.us/v2/users/{}".format(email)
    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    obj = {
            "action": "create",
            "user_info": {
                "email": "neeraj+2@goognu.com",
                "first_name": "Neeraj Goognu 2",
                "last_name": "Kumar",
                "password": "Neeraj@123",
                "type": 1,
                "feature": {
                    "zoom_phone": False
                }
                }
            }
    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    create_meeting = requests.get(url,headers=header)

    # print(create_meeting)
    # print("**"*30)
    # print(create_meeting.text)

    response = json.loads(create_meeting.text)

    return create_meeting.status_code, response


def assign_license_to_user(email):
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    print(round_off_datetme)

    headers = {"alg":"HS256", "typ":"JWT"}
    payload = {"iss":api_key,"exp":round_off_datetme}
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")
    
    
    url = "https://api.zoom.us/v2/users/{}".format(email)
    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    obj = {
            "type": 2,
            }
    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    response = requests.patch(url,json=obj,headers=header)

    response_code = response.status_code

    return response_code


def remove_license_to_user(email):
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    print(round_off_datetme)

    headers = {"alg":"HS256", "typ":"JWT"}
    payload = {"iss":api_key,"exp":round_off_datetme}
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")
    
    
    url = "https://api.zoom.us/v2/users/{}".format(email)
    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    obj = {
            "type": 1,
            }
    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    response = requests.patch(url,json=obj,headers=header)

    response_code = response.status_code

    return response_code


#call when meeting end
def inc_meeting_license_number():
    zoom_meeting_obj = ZoomLicenseDetails.objects.all().last()
    use_license =  zoom_meeting_obj.use_license
    ZoomLicenseDetails.objects.filter(id=zoom_meeting_obj.id).update(
        use_license = use_license-1
    )

    return 200


#call when meeting start
def dec_meeting_license_number():
    # zoom_meeting_obj = ZoomLicenseDetails.objects.all().last()

    # # total_license = zoom_meeting_obj.total_license
    # use_license =  zoom_meeting_obj.use_license

    # ZoomLicenseDetails.objects.filter(id=zoom_meeting_obj.id).update(
    #     # total_license = total_license-1,
    #     use_license = use_license+1
    # )

    return 200

'''
New TESTING CODE FOR OUTH
'''
import base64
client_id="3dHVIBCnT3iOMEXjzBJlsw"
client_secret="c4XmkIHpXKNbHeUvjLT5FBCCtbx8HBhq"
api_id = "LHl-9cYVTFGfMkqmlryYHQ"

def zoom_scheduled_meeting_test(request,title=None,description=None,start=None,end=None,attendees_list=None,zoom_user_email = None,token=None):
    now = datetime.datetime.now()
    email = settings.ZOOM_ADMIN_EMAIL
    access_token=token
    amsterdam_timezone = pytz.timezone('Asia/Kolkata')
    date_search = amsterdam_timezone.localize(now)
    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=5)
    round_off_datetme = round(experation_time.timestamp())
    zoom_password_random = random.randint(1000,9999)

    url = "https://api.zoom.us/v2/users/{}/meetings".format(zoom_user_email)
    obj = {"topic":title,"password":zoom_password_random,
            "settings":{"allow_multiple_devices":True,"auto_recording":"cloud","watermark":True},
            "type":1}
    header = {"authorization":"Bearer {}".format(access_token)}
    create_meeting = requests.post(url,json=obj,headers=header)
    response = create_meeting.text
    response_dict = json.loads(response)
    return response_dict,zoom_password_random


def create_zoom_user_test(name,email,password):
    data_dict = {}
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")

    url = "https://api.zoom.us/v2/users"
    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    obj = {
            "action": "create",
            "user_info": {
                "last_name": "",
                "type": 1,
                "feature": {
                    "zoom_phone": False
                }
                }
            }
    obj['user_info']['email'] = email
    obj['user_info']['first_name'] = name 
    obj['user_info']['password'] = password
    header = {"authorization":"Bearer {}".format(encoded_jwt)}
    create_user = requests.post(url,json=obj,headers=header)
    return create_user.text


def get_user_details_test(email):
   
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={api_id}"

    payload = {}
    headers = {
        'grant_type': 'authorization_code',
        'Authorization': f'Basic {encoded_credentials}',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    token=res['access_token']
    
    url = f"https://api.zoom.us/v2/users/{email}"
    payload = ""
    headers = {
    'Authorization': f'Bearer {token}',
   
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res=response.text
    res=json.loads(res)
    return response.status_code, res,token


def assign_license_to_user_test(email,token):
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    url = f"https://api.zoom.us/v2/users/{email}"
    payload = ""
    headers = {
    'Authorization': f'Bearer {token}',
   
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res=response.text
    res=json.loads(res)

    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    obj = {
            "type": 2,
        }
    
    response = requests.patch(url,json=obj,headers=headers)
    response_code = response.status_code
    return response_code


def remove_license_to_user_test(email,token):
    api_key = settings.ZOOM_API_KEY
    api_secret = settings.ZOOM_API_SECRET

    date_time = datetime.datetime.now()
    experation_time = date_time + datetime.timedelta(minutes=20)
    round_off_datetme = round(experation_time.timestamp())
    print(round_off_datetme)
    url = f"https://api.zoom.us/v2/users/{email}"
    payload = ""
    headers = {
    'Authorization': f'Bearer {token}',
   
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res=response.text
    res=json.loads(res)

    date = experation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = date_time + datetime.timedelta(days=100)
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    obj = {
            "type": 1,
        }
    
    response = requests.patch(url,json=obj,headers=headers)
    response_code = response.status_code
    return response_code

