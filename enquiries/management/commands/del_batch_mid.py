from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta,datetime
from batches.models import Batches
import os



class Command(BaseCommand):
    help = 'Validate the courses details, if course id=s complete or not.'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        print(now)

        batch_obj  = Batches.objects.all()

        for i in batch_obj:
            # print(i.id)
            Batches.objects.filter(id=i.id).update(
                zoom_meeting_id = None,
                zoom_meeting_password = None,
                zoom_bitly_link_instructer = None,
                zoom_bitly_link_student_mobile = None
            )
            print("Meeting id and Link cleared for Batch {}".format(i.id))