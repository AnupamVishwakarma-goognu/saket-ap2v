from urllib import response
from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from .models import AccessToken
from datetime import datetime, timedelta
from django.conf import settings
import jwt

# Create your views here.
def genrate_access_token_for_bluejeans(request):
    url = "https://api.bluejeans.com/oauth2/token?Password"

    payload = json.dumps({
        "grant_type": "password",
        "username": settings.BLUEJEANS_USERNAME,
        "password": settings.BLUEJEANS_PASSWORD
    })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        access_token = json_data['access_token']
        user = json_data['scope']['user']

        if AccessToken.objects.all():
            if access_token and user:
                AccessToken.objects.filter(id=1).update(
                    access_token = access_token,
                    user = user
                )
        else:
            enterprise = get_enterprise_id(user,access_token)
            if access_token and user and enterprise:
                x = AccessToken(
                    access_token = access_token,
                    user = user,
                    enterprise=enterprise
                )
                x.save()
    return HttpResponse(json_data)
    
def genrate_access_token(request):
    url = "https://api.bluejeans.com/oauth2/token?Password"

    payload = json.dumps({
        "grant_type": "password",
        "username": settings.BLUEJEANS_USERNAME,
        "password": settings.BLUEJEANS_PASSWORD
    })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        access_token = json_data['access_token']
        user = json_data['scope']['user']

        if AccessToken.objects.all():
            if access_token and user:
                AccessToken.objects.filter(id=1).update(
                    access_token = access_token,
                    user = user
                )
        else:
            enterprise = get_enterprise_id(user,access_token)
            if access_token and user and enterprise:
                x = AccessToken(
                    access_token = access_token,
                    user = user,
                    enterprise=enterprise
                )
                x.save()
    # return HttpResponse(json_data)
    return "OK"

def check_token(request):
    user_token_obj = AccessToken.objects.all().last()
    access_token = user_token_obj.access_token
    url = "https://api.bluejeans.com/oauth2/tokenInfo?access_token="+access_token

    payload={}
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return "OK"
        # return HttpResponse("json_data")
    else:
        res = genrate_access_token(request)
        return "OK"
        # return HttpResponse("json_data")

def get_enterprise_id(user,access_token):
    url = "https://api.bluejeans.com/v1/user/"+str(user)+"/enterprise_profile?access_token="+access_token

    payload={}
    files={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        enterprise_id = json_data['enterprise']
        return enterprise_id
    else:
        return 0



def scheduled_meeting(request,title=None,description=None,start=None,end=None,attendees_list=None,user_id = None):
    result = check_token(request)
    
    user_token_obj = AccessToken.objects.all().last()
    access_token = user_token_obj.access_token

    if user_id == None:
        user_id = user_token_obj.user

    from datetime import datetime
    start = int(datetime.timestamp(start))*1000
    end = int(datetime.timestamp(end))*1000

    url = "https://api.bluejeans.com/v1/user/"+str(user_id)+"/scheduled_meeting?access_token="+access_token+"&email=true"

    payload = json.dumps({
    "title": title,
    "description": description,
    "start": start,
    "end": end,
    "timezone": "Asia/Kolkata",
    "advancedMeetingOptions": {
      "autoRecord": True
    },
    "endPointType": "WEB_APP",
    "endPointVersion": "2.0",
    "attendees": attendees_list,
    "isLargeMeeting": True,
    "recurrencePattern": {
    "recurrenceType": "DAILY",
    "endDate": end,
    "recurrenceCount": 0,
    "frequency": 1,
    "daysOfWeekMask": 0,
    "dayOfMonth": 0,
    "weekOfMonth": "NONE",
    "monthOfYear": "NONE"
  },
    "isPersonalMeeting": False
    })
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    if response.status_code == 201:
        json_data = json.loads(response.text)

        numericMeetingId = json_data['numericMeetingId']
        attendeePasscode = json_data['attendeePasscode']

        print("Meeting id : ", numericMeetingId)
        print("Attendee Passcode : ", attendeePasscode)

        return numericMeetingId,attendeePasscode
    else:
        return HttpResponse("some is wrong while creating meeting")
    

def get_recording_compositeContentId(request,meeting_id,user_id=None):
    result = check_token(request)

    user_token_obj = AccessToken.objects.all().last()
    if user_id == None:
        user_id = user_token_obj.user
    access_token = user_token_obj.access_token

    url = "https://api.bluejeans.com/v1/user/"+str(user_id)+"/meeting_history/"+str(meeting_id)+"/recordings?access_token="+access_token

    payload={}
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response)
    json_data = json.loads(response.text)

    composite_content_id = []
    if response.status_code == 200:
        for i in json_data:
            c_id = i['compositeContentId']
            composite_content_id.append(c_id)
    
    return composite_content_id

def get_courses_recordings(request,composite_list,user_id=None):
    result = check_token(request)
    user_token_obj = AccessToken.objects.all().last()
    if user_id == None:
        user_id = user_token_obj.user
    access_token = user_token_obj.access_token

    course_recording_lis = []
    total_minute = 0

    for i in composite_list:
        composite_recording_data = {}
        url = "https://api.bluejeans.com/v1/user/"+str(user_id)+"/cms/"+str(i)+"?isDownloadable=true&access_token="+access_token
    
        payload={}
        headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        if 'created' in json_data:
            composite_recording_data['recorded_on']=datetime.fromtimestamp(int(json_data['created']/1000.0))
        else:
            composite_recording_data['recorded_on']=None

        if 'duration' in json_data['contentProperties']:
            composite_recording_data['length']=round((int(json_data['contentProperties']['duration'])/60),2)
        else:
            composite_recording_data['length']=0
        # composite_recording_data['url']=json_data['contentProperties']['levels'][0]['file']
        if 'contentUrl' in json_data:
            try:
                composite_recording_data['url']=json_data['contentProperties']['levels'][0]['file']
            except:
                composite_recording_data['url']=json_data['contentUrl']
        else:
            composite_recording_data['url']=None

        composite_recording_data['composite_id']=i
        composite_recording_data['user']=user_id
        course_recording_lis.append(composite_recording_data)

        if 'duration' in json_data['contentProperties']:
            total_minute = round((total_minute+int(json_data['contentProperties']['duration'])/60),2)
        else:
            total_minute=0
    return course_recording_lis,total_minute

def get_recordings_url_by_composite_id(request,composite_id,user):
    result = check_token(request)
    user_token_obj = AccessToken.objects.all().last()
    user_id = user
    access_token = user_token_obj.access_token

    url = "https://api.bluejeans.com/v1/user/"+str(user_id)+"/cms/"+str(composite_id)+"?isDownloadable=true&access_token="+access_token

    payload={}
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    try:
        url=json_data['contentProperties']['levels'][0]['file']
    except:
        url=json_data['contentUrl']

    return url


def create_user_instructor(request,name=None,id=None,reactive=None):
    result = check_token(request)
    user_token_obj = AccessToken.objects.all().last()
    access_token = user_token_obj.access_token
    enterprise_id = user_token_obj.enterprise

    default_email = settings.DEFAULT_INSTRUCTOR_EMAIL
    email_split = default_email.split("@")
    if reactive:
        import random
        random_number = random.randint(100,999)
        ren = str(random_number)
        id= str(id)+ren
    new_email = email_split[0]+"+"+str(id)+"@"+email_split[1]


    if name and new_email:
        url = "https://api.bluejeans.com/v1/enterprise/"+ str(enterprise_id)+"/users?access_token="+access_token

        payload = json.dumps({
            "emailId": new_email,
            "username": "",
            "firstName": name,
            "lastName": "",
            "company": settings.BLUEJEANS_COMPANY,
            "title": settings.BLUEJEANS_TITLE
        })
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        # print(response.text)
        # print(json_data)

        user_id = json_data['id']
    return user_id


def activate_user_room(request,user_id):
    result = check_token(request)
    user_token_obj = AccessToken.objects.all().last()
    access_token = user_token_obj.access_token
    enterprise_id = user_token_obj.enterprise

    url = "https://api.bluejeans.com/v1/user/"+str(user_id)+"/room?access_token="+access_token
    payload="{}"
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)

    moderatorPasscode = json_data['moderatorPasscode']
    return moderatorPasscode, json_data


def genrate_bitly_link(request,link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    print("------- Genrate Bitly Link --------")
    print(link)

    payload = json.dumps({
        "group_guid": settings.BITLY_GUID,
        "domain": "bit.ly",
        "long_url":link
    })

    headers = {
        'Authorization': 'Bearer '+settings.BITLY_ACCESS_TOKEN,
        'HOST': 'api-ssl.bitly.com',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_data = json.loads(response.text)
    link = json_data['link']
    return link


def get_zoom_recording_data(user_email = None):
    if user_email:
        api_key = settings.ZOOM_API_KEY
        api_secret = settings.ZOOM_API_SECRET

        date_time = datetime.now()
        experation_time = date_time + timedelta(minutes=20)
        round_off_datetme = round(experation_time.timestamp())
        print(round_off_datetme)

        headers = {"alg":"HS256", "typ":"JWT"}
        payload = {"iss":api_key,"exp":round_off_datetme}
        encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")

        # url = "https://api.zoom.us/v2/past_meetings/{}".format('94750059899')
        url = "https://api.zoom.us/v2/users/{}/recordings".format(user_email)
        header = {"authorization":"Bearer {}".format(encoded_jwt)}
        create_meeting = requests.get(url,headers=header)

        response = response_dict = json.loads(create_meeting.text)
        # print(type(response))

        return create_meeting.status_code, response



client_id="3dHVIBCnT3iOMEXjzBJlsw"
client_secret="c4XmkIHpXKNbHeUvjLT5FBCCtbx8HBhq"
api_id = "LHl-9cYVTFGfMkqmlryYHQ"
import base64
def get_zoom_recording_data_test(user_email = None):
    if user_email:
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
        url = "https://api.zoom.us/v2/users/{}/recordings".format(user_email)
        headers = {
        'Authorization': f'Bearer {token}',
        }
        create_meeting = requests.get(url,headers=headers)
        response = response_dict = json.loads(create_meeting.text)
        return create_meeting.status_code, response        