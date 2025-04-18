from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate
from batches.models import Batches
from demo.models import Demo
from datetime import datetime,timedelta
from django.utils import timezone
import pytz
from datetime import date
from bluejeans.views import get_recording_compositeContentId,get_courses_recordings


class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):
        now = date.today()

        # batch_obj_meeting_ids = Batches.objects.filter(start_date_time__gte = now, end_date_time__lte = now).values_list('meeting_id')
        batch_obj_meeting_ids = Batches.objects.all().values_list('meeting_id')

        for i in batch_obj_meeting_ids:
            try:
                batch_recording_composite_list = BatchRecordingsURL.objects.filter(meeting_id = int(i[0])).values_list('composite_id')

                batch_composite_list = []
                if batch_recording_composite_list:
                    for k in batch_recording_composite_list:
                        batch_composite_list.append(int(k[0]))
                

                batch_obj_user = Batches.objects.filter(meeting_id = int(i[0])).first()
                all_composite_id_list = get_recording_compositeContentId(self,i[0],batch_obj_user.instructors.blue_jeans_user_id)

                left_composite_list = list(set(all_composite_id_list)-set(batch_composite_list))

                print("all composite list : ", all_composite_id_list)
                print("batch_composite_list :",batch_composite_list)
                print("left_composite_list : ",left_composite_list)

                if left_composite_list:
                    all_recording_link_list = get_courses_recordings(self,left_composite_list,batch_obj_user.instructors.blue_jeans_user_id)
                    
                    for m in all_recording_link_list[0]:
                        x = BatchRecordingsURL(
                            batch=1,
                            meeting_id = i[0],
                            composite_id = m['composite_id'],
                            recording_on = m['recorded_on'],
                            link=m['url'],
                            duration=int(m['length'])
                        )
                        x.save()
                else:
                    print("-------- Nothing New Found --------------")
            except Exception as e:
                print(e)
        

        #-----------------------------------------------------------------for Demo Batch---------------------------
        print("-----------------------------------------------------------------Start for Demo Batch---------------------------")

        # batch_obj_meeting_ids = Demo.objects.filter(start_date_time__gte = now, end_date_time__lte = now).values_list('meeting_id')
        batch_obj_meeting_ids = Demo.objects.all().values_list('meeting_id')

        for i in batch_obj_meeting_ids:
            try:
                batch_recording_composite_list = BatchRecordingsURL.objects.filter(meeting_id = int(i[0])).values_list('composite_id')

                batch_composite_list = []
                if batch_recording_composite_list:
                    for k in batch_recording_composite_list:
                        batch_composite_list.append(int(k[0]))
                

                batch_obj_user = Demo.objects.filter(meeting_id = int(i[0])).first()
                all_composite_id_list = get_recording_compositeContentId(self,i[0],batch_obj_user.instructors.blue_jeans_user_id)

                left_composite_list = list(set(all_composite_id_list)-set(batch_composite_list))

                print("all composite list : ", all_composite_id_list)
                print("batch_composite_list :",batch_composite_list)
                print("left_composite_list : ",left_composite_list)

                if left_composite_list:
                    all_recording_link_list = get_courses_recordings(self,left_composite_list,batch_obj_user.instructors.blue_jeans_user_id)
                    
                    for m in all_recording_link_list[0]:
                        x = BatchRecordingsURL(
                            batch=2,
                            meeting_id = i[0],
                            composite_id = m['composite_id'],
                            recording_on = m['recorded_on'],
                            link=m['url']
                        )
                        x.save()
                else:
                    print("---------- Nothing New Found -------------")
            except Exception as e:
                print(e)

        y = RecordingProcessDate(
            date = timezone.now()
        )
        y.save()