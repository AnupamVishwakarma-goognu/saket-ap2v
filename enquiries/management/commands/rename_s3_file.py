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

class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):
        batch_recording_url_obj = BatchRecordingsURL.objects.filter(download=True)
        print(batch_recording_url_obj.count())
        for i in batch_recording_url_obj:
            # print(str(i.recording_on.strftime('%Y%m%d%H%M%S')))
            new_date = str(i.recording_on.strftime('%Y%m%d%H%M%S'))

            year = i.recording_on.date().year
            month = i.recording_on.date().month
            day = i.recording_on.date().day
            old_date = str(year)+str(month)+str(day)
            # old_date = str(i.recording_on.strftime('%Y%m%d'))
            try:
                batch_id = Demo.objects.filter(meeting_id= i.meeting_id).first().id
            except:
                batch_id = Batches.objects.filter(meeting_id = i.meeting_id).first().id

            #---------------------------------rename process start--------------------------------
            ACCESS_KEY = settings.ACCESS_KEY
            SECRET_KEY = settings.AWS_SECRET_KEY
            BUCKETNAME = settings.BUCKETNAME

            if int(i.batch) == 1:
                old_s3_file_name = 'b/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(old_date)+'.mp4'
            else:
                old_s3_file_name = 'd/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(old_date)+'.mp4'



            if int(i.batch) == 1:
                new_s3_file_name = 'batch/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(new_date)+str('_')+str(i.duration)+'.mp4'
            else:
                new_s3_file_name = 'demo/'+str(batch_id)+str('/')+str(i.meeting_id)+str('_')+str(i.composite_id)+str('_')+str(new_date)+str('_')+str(i.duration)+'.mp4'
            # local_file = file_name
            bucket = BUCKETNAME
            new_s3_file = new_s3_file_name

            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
            # s3.meta.client.copy(bucket, "b2/70/597694353_28194862_20210825082012_25A.mp4").copy_from(CopySource="b/70/597694353_28194862_20210825082012_25.mp4")
            copy_source = {
                'Bucket': bucket,
                'Key': old_s3_file_name
            }
            s3.copy(copy_source, bucket, new_s3_file_name) #new location and name


