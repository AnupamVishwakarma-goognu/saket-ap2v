from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate
from batches.models import Batches
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

class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):
        batch_recording_url_obj = BatchRecordingsURL.objects.filter(download=False)
        print(batch_recording_url_obj.count())
        for i in batch_recording_url_obj:
            # print(str(i.recording_on.strftime('%Y%m%d%H%M%S')))
            date = str(i.recording_on.strftime('%Y%m%d%H%M%S'))
            try:
                batch_id = Demo.objects.filter(meeting_id= i.meeting_id).first().id
            except:
                batch_id = Batches.objects.filter(meeting_id = i.meeting_id).first().id
            # print(i.link)

            dwn_link = i.recording_on
            file_name = settings.TEMP_RECORDING_STORE+str(i.meeting_id)+str('_')+str(i.composite_id)+str(date)+'.mp4'
            r = requests.get(i.link, stream = True)
            # print(r)
            r.raw.decode_content = True
            with open(file_name,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
            BatchRecordingsURL.objects.filter(id=i.id).update(
                download=True
            )
            print("Recording save successfully at : ",file_name)

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
            SECRET_KEY = settings.SECRET_KEY
            BUCKETNAME = settings.BUCKETNAME

            if int(i.batch) == 1:
                s3_file_name = 'batch/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(date)+str('_')+str(duration)+'.mp4'
            else:
                s3_file_name = 'demo/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(date)+str('_')+str(duration)+'.mp4'

            local_file = file_name
            bucket = BUCKETNAME
            s3_file = s3_file_name
    
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

            try:
                s3.upload_file(local_file, bucket, s3_file)
                print("****Upload Successful-")
                BatchRecordingsURL.objects.filter(id=i.id).update(
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