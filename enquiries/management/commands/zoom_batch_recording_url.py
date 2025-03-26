from traceback import print_tb
from django.core.management.base import BaseCommand, CommandError
from numpy import record
from classroom.views import recording_play
from core.models import BatchRecordingsURL,RecordingProcessDate,ZoomRecordingURL
from batches.models import Batches,ZoomMeetingIdUserBatch
from demo.models import Demo
from datetime import datetime,timedelta
from django.utils import timezone
import pytz
from datetime import date
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings
from bluejeans.views import get_zoom_recording_data,get_zoom_recording_data_test


class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        print(now)

        amsterdam_timezone = pytz.timezone('Asia/Kolkata')
        date_search = amsterdam_timezone.localize(now)
        date_search = date_search - timedelta(days=1)
        print("Searching From: ",date_search.date())

        batch_obj_meeting_ids = Batches.objects.filter(end_date_time__gte = date_search)
        # batch_obj_meeting_ids = Batches.objects.all().values_list('zoom_meeting_id')

        batch_meeting_dict = {}
        inst_email_list = []
        # for i in batch_obj_meeting_ids:
        #     if len(i.zoom_meeting_id) > 1:
        #         batch_meeting_dict[i.zoom_meeting_id] = i.id

        # print(batch_meeting_dict)

        #get 3 days old data 
        olddate = now-timedelta(days = 7)
        # batchMeetingId_obj = ZoomMeetingIdUserBatch.objects.all()
        batchMeetingId_obj = ZoomMeetingIdUserBatch.objects.filter(date__gte = olddate)
        print(batchMeetingId_obj)

        for k in batchMeetingId_obj:
            if k.meeting_type == '1':
                print(k)
                batch_id = k.batch.id
                meeting_id = k.meeting_id
                inst_email = k.batch.instructors.email
                batch_meeting_dict[meeting_id] = batch_id
                inst_email_list.append(inst_email)
        
        

        zoom_user_list = list(set(inst_email_list))
        # zoom_user_list = ["ashu@ap2v.com"]

        zoom_user_list.append("neeraj@goognu.com")
        zoom_user_list.append("ashu@ap2v.com")

        for i in zoom_user_list:
            # status_code,responce = get_zoom_recording_data(i)
            status_code,responce = get_zoom_recording_data_test(i)
            print(responce)
            if status_code == 200:
                all_meeting = responce['meetings']
                for j in all_meeting:
                    file_url=None
                    file_url_list = []
                    composite_uuid_id = j['uuid']
                    meeting_id = j['id']
                    duration = j['duration']       
                            

                    if not ZoomRecordingURL.objects.filter(meeting_id = meeting_id,composite_uuid_id = composite_uuid_id).exists():
                        if ZoomMeetingIdUserBatch.objects.filter(meeting_id = meeting_id).exists():
                            if len(j["recording_files"]) > 1:
                                print(j)

                                for flu in range(len(j["recording_files"])):
                                    if j['recording_files'][flu]['file_type'] == "MP4":
                                        file_url = j['recording_files'][flu]['download_url']
                                        file_url_list.append(file_url)
                                    # elif j['recording_files'][1]['file_type'] == "MP4":
                                    #     file_url = j['recording_files'][1]['download_url']
                                if file_url:
                                    recording_on = j['start_time']
                                    recording_on = datetime.strptime(recording_on,"%Y-%m-%dT%H:%M:%SZ")
                                    recording_on = recording_on+timedelta(hours=5.30)

                                    # print(file_url)
                                    print("Recording URL Fetching for Composite Id : {}, Meeting Id : {}".format(composite_uuid_id,meeting_id))
                                    print("URL: ",file_url)

                                    batch_id = batch_meeting_dict[str(meeting_id)]
                                    print(batch_id)
                                    batch_obj = Batches.objects.filter(id=batch_id).first()

                                    for fl in file_url_list:
                                        x = ZoomRecordingURL(
                                            batch = '1',
                                            meeting_id = meeting_id,
                                            composite_uuid_id = composite_uuid_id,
                                            recording_on = recording_on,
                                            link = fl,
                                            date = datetime.now(),
                                            duration = duration
                                        )
                                        x.save()
                                        print(x.id)
                                else:
                                    print("File Not Ready of Meeting ID : {}, Composite ID : {}".format(meeting_id,composite_uuid_id))
                        else:
                            print("Meeting Id is not exists in our batch db...")
                    else:
                        print("NOTE: Recording Alredy Fetched of this URL...")
                    
                    print("*************  END for Composite id: {}, Meeting id : {} **************".format(composite_uuid_id,meeting_id))

