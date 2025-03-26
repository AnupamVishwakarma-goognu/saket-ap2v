from django.core.management.base import BaseCommand
from enquiries.models import Enquiries,EnquiryCourses
import logging
logger = logging.getLogger('junk_enq_log')

class Command(BaseCommand):
    help = 'This script delete those enquiry which marked as junk, also delte its related courses(Enquiry Course).'
    def handle(self, *args, **kwargs):
        junk_enq_obj = Enquiries.objects.filter(junk = True)
        print(junk_enq_obj)

        for i in junk_enq_obj:
            id = i.id
            date = (i.added_on.strftime('%d-%m-%Y %H:%M:%S'))
            name = i.full_name
            mobile = i.mobile
            email = i.email

            # f= open('/tmp/junk_enquiry.txt',"a+")
            # f= open('D:/junk_enquiry.txt',"a+")
            line = str(id)+"-> "+str(date)+"/"+name+"/"+mobile+"/"+email
            print(line)
            
            try:
                EnquiryCourses.objects.filter(enquiry_id = i.id).delete()
                Enquiries.objects.filter(id=i.id).delete()
                # f.write(line)
                # f.write("\n")
                logger.info(line)
            except Exception as e:
                print(e)
            