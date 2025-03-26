from urllib import response
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate
from django.utils import timezone
from enquiries.models import Enquiries
from courses.models import Courses
from batches.models import Batches
import datetime
import pytz

import jwt
import datetime
import requests
import json
import random
from bluejeans.views import genrate_bitly_link
import base64
client_id="3dHVIBCnT3iOMEXjzBJlsw"
client_secret="c4XmkIHpXKNbHeUvjLT5FBCCtbx8HBhq"
api_id = "LHl-9cYVTFGfMkqmlryYHQ"

class Command(BaseCommand):
    help = 'This Script Will Fetch the Running Batch and Create a Class Link on Zoom and Meeting id and Save it to Batch Model...'
    
    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        email = settings.ZOOM_ADMIN_EMAIL
        api_key = settings.ZOOM_API_KEY
        api_secret = settings.ZOOM_API_SECRET

        amsterdam_timezone = pytz.timezone('Asia/Kolkata')
        date_search = amsterdam_timezone.localize(now)
        print("Now : ",date_search.date())

        batch_obj = Batches.objects.filter(end_date_time__gte = date_search)
        print(batch_obj)
        for i in batch_obj:
            if i.id == 184:
                if not i.zoom_response_logs:
                    print("ID : ",i.id, " Start Date Time : ",i.start_date_time, " End Date Time : ",i.end_date_time)

                    start_time = i.start_date_time

                    batch_start_date_time = datetime.datetime.combine(date_search.date(), start_time.time())                        
                    #Batch Start Date time
                    batch_start_date_time = batch_start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print("Batch Start Datetime Zoom Format : ",batch_start_date_time)          

                    batch_end_date_time = i.end_date_time + datetime.timedelta(days=100)                                            
                    #Batch End Date time
                    batch_end_date_time = batch_end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print("Batch End Datetime Zoom Format : ",batch_end_date_time)

                    course_list = []
                    for j in i.courses.all():
                        course_list.append(j.name)

                    batch_title = " & ".join(course_list)                                                                           
                    #Batch Title
                    print("Batch Title : ",batch_title)
                    
                    date_time = datetime.datetime.now()
                    experation_time = date_time + datetime.timedelta(minutes=5)
                    round_off_datetme = round(experation_time.timestamp())
                    credentials = f"{client_id}:{client_secret}"
                    encoded_credentials = base64.b64encode(credentials.encode()).decode()
                    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={api_id}"

                    payload = {"exp":round_off_datetme}
                    headers = {
                    'grant_type': 'authorization_code',
                    'Authorization': f'Basic {encoded_credentials}',
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    res = json.loads(response.text)
                    token=res['access_token']


                    zoom_password_random = random.randint(1000,9999)

                    email = i.instructors.zoom_email

                    url = "https://api.zoom.us/v2/users/{}/meetings".format(email)
                    obj = {"topic":batch_title,"starttime":batch_start_date_time,"duration":70,"password":zoom_password_random,
                            "recurrence":{"end_date_time":batch_end_date_time,"type":1},
                            "settings":{"allow_multiple_devices":True,"auto_recording":"cloud","watermark":True},
                            "type":3}
                    header = {"authorization":"Bearer {}".format(token)}
                    create_meeting = requests.post(url,json=obj,headers=header)
                    response = create_meeting.text

                    response_dict = json.loads(response)
                    print("RESPONSE 78: ",response_dict)

                    zoom_inst_url = response_dict['start_url']
                    zoom_stu_url = response_dict['join_url']

                    bitly_int_url = genrate_bitly_link(self,zoom_inst_url)
                    bitly_stu_url = genrate_bitly_link(self,zoom_stu_url)

                    Batches.objects.filter(id = i.id).update(
                        zoom_meeting_id = response_dict['id'],
                        zoom_meeting_password = zoom_password_random, 
                        zoom_bitly_link_instructer = bitly_int_url, 
                        zoom_bitly_link_student_mobile = bitly_stu_url, 
                        zoom_response_logs = response_dict
                    )

            else:
                print("!!! Note : Zoom Meeting already created for batch {} ...".format(i.id))