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
            if i.zoom_response_logs:
                Batches.objects.filter(id = i.id).update(
                    zoom_meeting_id = None,
                    zoom_meeting_password = None, 
                    zoom_bitly_link_instructer = None, 
                    zoom_bitly_link_student_mobile = None, 
                    zoom_response_logs = None
                )

            else:
                print("!!! Note : Zoom Meeting not genrated {} ...".format(i.id))