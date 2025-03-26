from django.core.management.base import BaseCommand, CommandError
from enquiries.models import Followups,Enquiries
from enrolls.models import Enrollments,Installments
from datetime import datetime,timedelta
from django.db.models import Sum

class Command(BaseCommand):
    help = '''Anquira Summary Report
        Total pending followup:
        Total overdue followups:
        How many new leads received:
        How many Admissions done: 0
        How much Training amount received -
        Is there any pending followup?
        Is there any overdue followup?
        '''


    def handle(self, *args, **options):
        now = datetime.now()
        yesterday=now - timedelta(days=1)
        last_week=now - timedelta(days=7)

        data = {}
        pending_followups = Followups.objects.filter(discard=False).values_list('followupid').distinct().count()
        overdue_followups = Followups.objects.filter(discard=False,next_followup__lte=now).values_list('followupid').distinct().count()
        data['Pending Folloups']=pending_followups
        data['Overdue Folloups'] = overdue_followups

        new_leads_in_1day = Enquiries.objects.filter(added_on__gte=yesterday).count()
        new_leads_in_7day = Enquiries.objects.filter(added_on__gte=last_week).count()
        data['New Leads(24hrs)'] = new_leads_in_1day
        data['New Leads(7Days)']=new_leads_in_7day        
        
        new_enrollments_in_1day = Enrollments.objects.filter(added_on__gte=yesterday).count()
        new_enrollments_in_7day = Enrollments.objects.filter(added_on__gte=last_week).count()
        data['New Enrolls(24Hrs)']=new_leads_in_1day
        data['New Enrolls(7Days)']=new_enrollments_in_7day

        amount_in_1day = Installments.objects.filter(updated_on__gte=yesterday,paid_unpaid=True).aggregate(sum=Sum('installment'))['sum']
        amount_in_7day = Installments.objects.filter(updated_on__gte=last_week,paid_unpaid=True).aggregate(sum=Sum('installment'))['sum']
        data['Amount Collected(24Hrs)']=amount_in_1day if amount_in_1day else 0
        data['Amount Collected(7Days)']=amount_in_7day if amount_in_7day else 0

        pending_followups = Followups.objects.filter(next_followup__gte=now,discard=False).values_list('followupid').distinct().count()
        overdue_folloups = Followups.objects.filter(next_followup__lte=now,discard=False).values_list('followupid').distinct().count()
        data['Pending Followups']=pending_followups
        data['OverDue Followups']=overdue_followups

        for k, v in data.items():
            print('{k:25} ==> {v:10}'.format(k=k,v=v))
            print('-'*40)
            
