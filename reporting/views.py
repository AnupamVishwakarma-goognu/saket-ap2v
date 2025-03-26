from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
import json
from enquiries.models import Followups,Enquiries
from datetime import date,timedelta
from django.db.models import Q
from enrolls.models import Enrollments,Installments
from users.models import CustomUserModel as User
from django.db.models import Sum
from datetime import date, timedelta
from dateutil import parser
from anquira_v2.decorators import custome_check
from django.contrib.auth.decorators import login_required



class Reporting(View):
    def get_followups(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        followups_obj = Followups.objects.all()
        if counselor:
            followups_obj = followups_obj.filter(assigned_user=counselor)
        if start_date:
            followups_obj = followups_obj.filter(added_on__gte=start_date)
        if end_date:
            followups_obj = followups_obj.filter(added_on__lte=end_date)

        followups_count = followups_obj.count()
        return followups_count
    
    def get_overdue(self,counselor=None):
        followups_obj = Followups.objects.all()
        followups_obj = followups_obj.filter(added_on__gte = date.today())
        overdue = followups_obj.filter(followupid__added_on__gt = date.today() - timedelta(days=1),followupid__added_on__lt = date.today())
        if counselor:
            overdue =  overdue.filter(assigned_user=counselor)
        overdue = overdue.count()
        return overdue

    def get_new_enq(self,counselor=None, start_date=None, end_date=None):
        from datetime import datetime, timedelta
        if end_date: 
            end_date = end_date + timedelta(days=1)
        enq_obj = Enquiries.objects.all()
        if counselor:
            enq_obj = enq_obj.filter(assigned_by = counselor)
        if start_date:
            enq_obj = enq_obj.filter(assigned_on__gte=start_date)
        if end_date:
            enq_obj = enq_obj.filter(assigned_on__lte=end_date)
        new_enq = enq_obj.count()
        return new_enq

    def get_duplicate_enq(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        dup_enq_obj = Enquiries.objects.filter(added_on__gte=date.today())
        if counselor:
            dup_enq_obj = dup_enq_obj.filter(assigned_by = counselor)
        if start_date:
            dup_enq_obj = dup_enq_obj.filter(added_on__gte=start_date)
        if end_date:
            dup_enq_obj = dup_enq_obj.filter(added_on__lte=end_date)
        
        duplicate_enq = 0

        for i in dup_enq_obj:
            dup_enq = dup_enq_obj.filter(Q(email = i.email) | Q(mobile=i.mobile)).exclude(id=i.id)
            if dup_enq:
                duplicate_enq=duplicate_enq+int(dup_enq.count())
        return duplicate_enq

    def get_enroll_count(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        enroll_obj = Enrollments.objects.all()
        if counselor:
            enroll_obj = enroll_obj.filter(registered_by = counselor)
        if start_date:
            enroll_obj = enroll_obj.filter(added_on__gte=start_date)
        if end_date:
            enroll_obj = enroll_obj.filter(added_on__lte=end_date)

        enroll_count = enroll_obj.count()
        return enroll_count

    def get_amount_received(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        installment_obj = Installments.objects.filter(fee_type = 1)

        if counselor:
            installment_obj = installment_obj.filter(enrollmentid__registered_by = counselor)
        if start_date:
            installment_obj = installment_obj.filter(paid_on__gte=start_date)
        if end_date:
            installment_obj = installment_obj.filter(paid_on__lt=end_date)

        amount_received = 0
        today_paid = installment_obj.filter(paid_unpaid=True)
        for i in today_paid:
            amount = i.installment
            amount_received = amount_received+amount
        return amount_received

    def get_amount_pending(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        installment_obj = Installments.objects.filter(fee_type = 1)

        if counselor:
            installment_obj = installment_obj.filter(enrollmentid__registered_by = counselor)
        if start_date:
            installment_obj = installment_obj.filter(added_on__gte=start_date)
        if end_date:
            installment_obj = installment_obj.filter(added_on__lte=end_date)

        amount_pending = 0
        today_paid = installment_obj.filter(paid_unpaid=False)
        for i in today_paid:
            amount = i.installment
            amount_pending = amount_pending+amount
        return amount_pending

    def get_unattended_enq(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        enq_followups_obj = Enquiries.objects.all()

        if counselor:
            enq_followups_obj = enq_followups_obj.filter(assigned_by = counselor)
        if start_date:
            enq_followups_obj = enq_followups_obj.filter(added_on__gte=start_date)
        if end_date:
            enq_followups_obj = enq_followups_obj.filter(added_on__lte=end_date)

        unattended_enq = enq_followups_obj.filter(attended=False).count()
        if unattended_enq > 0:
            print("Is there any pending follow-up : Yes -",unattended_enq)
        else:
            print("Is there any pending follow-up : No")
        return unattended_enq

    def get_dropped_enrollment(self,counselor=None, start_date=None, end_date=None):
        if end_date: 
            end_date = end_date + timedelta(days=1)
        enroll_obj = Enrollments.objects.all()
        print(enroll_obj)
        if counselor:
            enroll_obj = enroll_obj.filter(registered_by = counselor)
            enroll_obj = enroll_obj.filter(dropped=True)
            print(enroll_obj)
        if start_date:
            enroll_obj = enroll_obj.filter(dropped_on__gte=start_date)
            print(enroll_obj)
        if end_date:
            enroll_obj = enroll_obj.filter(dropped_on__lt=end_date)
            print(enroll_obj)

        enroll_dropped_count = enroll_obj.count()
        print(enroll_dropped_count)
        return enroll_dropped_count




@login_required(login_url = '/')
@custome_check()
def report(request):
    ctx = {}
    ctx['counselor_obj'] = User.objects.filter(user_type="counselor")
    ctx['report_active'] = 'checked'

    return render(request,"report.html",ctx)

def get_report(request):
    import datetime
    ctx={}
    all_day_report = []
    ctx['report_active'] = 'checked'

    counselor = request.GET.get("counselor",None)
    start_date = request.GET.get("fromDate",None)
    end_date = request.GET.get("toDate",None)

    total_end_date = parser.parse(end_date)

    ctx['name'] = User.objects.filter(id=counselor).first().first_name
    class_obj = Reporting()

    a1 = class_obj.get_followups(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_followups'] = a1

    b1 = class_obj.get_overdue(counselor=counselor)
    ctx['total_overdue'] = b1

    c1 = class_obj.get_new_enq(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_new_enq'] = c1

    d1 = class_obj.get_duplicate_enq(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_duplicate_enq'] = d1

    e1 = class_obj.get_enroll_count(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_enroll_count'] = e1

    f1 = class_obj.get_amount_received(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_amount_received'] = f1

    g1 = class_obj.get_amount_pending(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_amount_pending'] = g1

    h1 = class_obj.get_unattended_enq(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_unattended_enq'] = h1

    i1 = class_obj.get_dropped_enrollment(counselor=counselor,start_date=start_date,end_date=total_end_date)
    ctx['total_dropped_enrollment'] = i1



# ------------------------------------------------------ Daily Report Genrateting process--------------------------------------------------------------
    # start_date = datetime.date.fromisoformat(start_date)
    # end_date = datetime.date.fromisoformat(end_date)

    start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()

    delta = end_date - start_date

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)

        date_data = {}
        date_data['date'] = day


        a = class_obj.get_followups(counselor=counselor,start_date=day,end_date=day)
        date_data['followups'] = a

        b = class_obj.get_overdue(counselor=counselor)
        date_data['overdue'] = b

        c = class_obj.get_new_enq(counselor=counselor,start_date=day,end_date=day)
        date_data['new_enq'] = c

        d = class_obj.get_duplicate_enq(counselor=counselor,start_date=day,end_date=day)
        date_data['duplicate_enq'] = d

        e = class_obj.get_enroll_count(counselor=counselor,start_date=day,end_date=day)
        date_data['enroll_count'] = e

        f = class_obj.get_amount_received(counselor=counselor,start_date=day,end_date=day)
        date_data['amount_received'] = f

        g = class_obj.get_amount_pending(counselor=counselor,start_date=day,end_date=day)
        date_data['amount_pending'] = g

        h = class_obj.get_unattended_enq(counselor=counselor,start_date=day,end_date=day)
        date_data['unattended_enq'] = h

        i = class_obj.get_dropped_enrollment(counselor=counselor,start_date=day,end_date=day)
        date_data['dropped_enrollment'] = i

        all_day_report.append(date_data)

    ctx['all_day_report']=all_day_report
    ctx['counselor_obj'] = User.objects.filter(user_type="counselor")
    return render(request,"report.html",ctx)


@login_required(login_url = '/')
@custome_check()
def fee_collection(request):
    ctx={}
    ctx['fee_active'] = 'checked'
    ctx['counselor_obj'] = User.objects.filter(user_type="counselor")

    start_date = request.GET.get("fee_fromDate",None)
    end_date = request.GET.get("fee_toDate",None)

    if not end_date:
        end_date = date.today()
    if start_date and end_date:

        total_installments_discussed_fee = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,fee_type=1).aggregate(Sum('installment'))
        ctx['total_fee'] = total_installments_discussed_fee['installment__sum']

        paid_installments_discussed_fee = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,paid_unpaid=True,fee_type=1).aggregate(Sum('installment'))
        ctx['paid_fee'] = paid_installments_discussed_fee['installment__sum']

        unpaid_installments_discussed_fee = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,paid_unpaid=False,fee_type=1).aggregate(Sum('installment'))
        ctx['unpaid_fee'] = unpaid_installments_discussed_fee['installment__sum']

        count_installments_discussed_fee = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,fee_type=1).count()
        ctx['total_fee_count'] = count_installments_discussed_fee

        total_fee_paid_count = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,paid_unpaid=True,fee_type=1).count()
        ctx['total_fee_paid_count'] = total_fee_paid_count

        total_fee_unpaid_count = Installments.objects.filter(added_on__gte = start_date,added_on__lte=end_date,paid_unpaid=False,fee_type=1).count()
        ctx['total_fee_unpaid_count'] = total_fee_unpaid_count

        ctx['start_date'] = start_date
        ctx['end_date'] = end_date

    return render(request,"report.html",ctx)