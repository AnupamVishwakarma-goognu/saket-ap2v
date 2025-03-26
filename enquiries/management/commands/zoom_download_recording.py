from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate,ZoomRecordingURL
from batches.models import Batches,ZoomMeetingIdUserBatch
from demo.models import Demo
from datetime import datetime,timedelta
from django.utils import timezone
import pytz
from datetime import date
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings
import urllib
import requests
import shutil
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError
import os
from moviepy.editor import VideoFileClip
import jwt
import random

class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):

        api_key = settings.ZOOM_API_KEY
        api_secret = settings.ZOOM_API_SECRET

        date_time = datetime.now()
        # experation_time = date_time + timedelta(minutes=20)\
        experation_time = date_time + timedelta(days=20)
        round_off_datetme = round(experation_time.timestamp())
        print(round_off_datetme)

        headers = {"alg":"HS256", "typ":"JWT"}
        payload = {"iss":api_key,"exp":round_off_datetme}
        encoded_jwt = jwt.encode(payload,api_secret,algorithm="HS256")


        batch_recording_url_obj = ZoomRecordingURL.objects.filter(download=False)
        print("Total Undownload Recording Found : ",batch_recording_url_obj.count())
        for i in batch_recording_url_obj:
            composite_id_int = random.randint(10000000,99999999)
            # print(str(i.recording_on.strftime('%Y%m%d%H%M%S')))
            date = str(i.recording_on.strftime('%Y%m%d%H%M%S'))
            try:
                batch_id = Demo.objects.filter(meeting_id= i.meeting_id).first().id
            except:
                batch_id = ZoomMeetingIdUserBatch.objects.filter(meeting_id = i.meeting_id).first().batch.id
            print(i.link)

            dwn_link = i.recording_on
            file_name = settings.TEMP_RECORDING_STORE+str(i.meeting_id)+str('_')+str(composite_id_int)+str(date)+'.mp4'
            zoom_link = i.link+"?access_token="+encoded_jwt
            r = requests.get(zoom_link, stream = True)
            print(r)
            r.raw.decode_content = True
            try:
                with open(file_name,'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                
                ZoomRecordingURL.objects.filter(id=i.id).update(
                    download=True
                )
                print("Recording save successfully at : ",file_name)
            except Exception as e:
                print(e)

            try:
                clip = VideoFileClip(file_name)
                duration = int((clip.duration)/60)
                print("Duration of local is :", duration)
                del clip
            except Exception as e:
                print(e)
                duration = i.duration

            #---------------------------------upload process start--------------------------------
            ACCESS_KEY = settings.ACCESS_KEY
            SECRET_KEY = settings.AWS_SECRET_KEY
            BUCKETNAME = settings.BUCKETNAME

            if int(i.batch) == 1:
                s3_file_name = 'batch/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(composite_id_int)+str('_')+str(date)+str('_')+str(duration)+'.mp4'
            else:
                s3_file_name = 'demo/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(composite_id_int)+str('_')+str(date)+str('_')+str(duration)+'.mp4'

            local_file = file_name
            bucket = BUCKETNAME
            s3_file = s3_file_name
    
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

            try:
                s3.upload_file(local_file, bucket, s3_file)
                print("****Upload Successful-")
                ZoomRecordingURL.objects.filter(id=i.id).update(
                    upload=True
                )

                try:
                    os.remove(file_name)
                except Exception as e:
                    print(e)
            except FileNotFoundError:
                print("****The file was not found")
            except NoCredentialsError:
                print("****Credentials not available")