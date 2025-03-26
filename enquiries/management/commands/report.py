from django.core.management.base import BaseCommand
# from django.utils import timezone
from datetime import date,timedelta
import pytz
from django.utils import timezone as tz
from enquiries.models import Enquiries
from users.models import CustomUserModel as User
from users.models import CounselorPreferences
import random
from reporting.views import Reporting
from communication.views import send_anquira_report_email


class Command(BaseCommand):
    help = 'Daily Basic Anquira Report'

    def handle(self, *args, **kwargs):
        counselor_report = []
        class_obj = Reporting()
        overall_report = {}

        overall_report['name']="Overall"

        today_folloups = class_obj.get_followups(start_date=date.today())
        overall_report['today_folloups']=today_folloups

        today_overdue = class_obj.get_overdue()
        overall_report['today_overdue']=today_overdue

        today_enquires = class_obj.get_new_enq(start_date=date.today())
        overall_report['today_enquires']=today_enquires

        today_duplicate_enquires = class_obj.get_duplicate_enq(start_date=date.today())
        overall_report['today_duplicate_enquires']=today_duplicate_enquires

        today_enrollment = class_obj.get_enroll_count(start_date=date.today())
        overall_report['today_enrollment']=today_enrollment

        today_amount_received = class_obj.get_amount_received(start_date=date.today())
        overall_report['today_amount_received']=today_amount_received

        today_pending_amount = class_obj.get_amount_pending(start_date=date.today())
        overall_report['today_pending_amount']=today_pending_amount

        pending_followup = class_obj.get_unattended_enq(start_date=date.today())
        overall_report['pending_followup']=pending_followup

        dropped_enrollment = class_obj.get_dropped_enrollment(start_date=date.today())
        overall_report['dropped_enrollment']=dropped_enrollment

        counselor_report.append(overall_report)

        counselor_user_obj = User.objects.filter(user_type="counselor")
        for i in counselor_user_obj:

            if CounselorPreferences.objects.filter(user=i.id).exists():
            
                counselor_report_dict = {}
                counselor_report_dict['name'] = i.first_name
                
                today_folloups = class_obj.get_followups(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_folloups']=today_folloups

                today_overdue = class_obj.get_overdue(counselor=i.id)
                counselor_report_dict['today_overdue']=today_overdue

                today_enquires = class_obj.get_new_enq(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_enquires']=today_enquires

                today_duplicate_enquires = class_obj.get_duplicate_enq(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_duplicate_enquires']=today_duplicate_enquires

                today_enrollment = class_obj.get_enroll_count(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_enrollment']=today_enrollment

                today_amount_received = class_obj.get_amount_received(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_amount_received']=today_amount_received

                today_pending_amount = class_obj.get_amount_pending(counselor=i.id,start_date=date.today())
                counselor_report_dict['today_pending_amount']=today_pending_amount

                pending_followup = class_obj.get_unattended_enq(counselor=i.id,start_date=date.today())
                counselor_report_dict['pending_followup']=pending_followup

                dropped_enrollment = class_obj.get_dropped_enrollment(counselor=i.id,start_date=date.today())
                counselor_report_dict['dropped_enrollment']=dropped_enrollment

                counselor_report.append(counselor_report_dict)
            #print(counselor_report)

        send_anquira_report_email(counselor_report)
