from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate
from django.utils import timezone
from enquiries.models import Enquiries
from courses.models import Courses

class Command(BaseCommand):
    help = 'Change the Update_on of enquiry according to added_on'

    def handle(self, *args, **kwargs):
       
        course_obj = Courses.objects.all()

        for i in course_obj:
            Courses.objects.filter(id=i.id).update(
                original_price=22499
            )
            
        print("All Anquira Course Original(With out discount) Price Updated to 22499 ")