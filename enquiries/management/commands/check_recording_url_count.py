from django.core.management.base import BaseCommand, CommandError
from core.models import BatchRecordingsURL,RecordingProcessDate,CommanModal
from datetime import datetime,timedelta
from communication.views import send_recording_urls_count_mail

class Command(BaseCommand):
    help = 'Check the daily downloadable recording progress'

    def handle(self, *args, **kwargs):

        batch_recording_urls_count = BatchRecordingsURL.objects.all().count()
        print("Total Recording URL Count Fount: ",batch_recording_urls_count)

        comman_model_obj = CommanModal.objects.all().first()    

        if comman_model_obj:
            if comman_model_obj.last_recording_url_count == batch_recording_urls_count:
                print("Sending Alert Mail....")
                send_recording_urls_count_mail()
            else:
                print("Everything is ok. :-)")
                CommanModal.objects.filter(id=comman_model_obj.id).update(
                    last_recording_url_count = batch_recording_urls_count
                )
        else:
            print("Saveing Count First Time.")
            x = CommanModal(
                last_recording_url_count = batch_recording_urls_count
            )
            x.save()