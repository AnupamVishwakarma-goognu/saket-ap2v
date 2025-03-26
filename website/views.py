from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from enquiries.models import Enquiries,Followups
from datetime import datetime, timedelta
from enrolls.models import Enrollments,Installments
from batches.models import Batches
from django.db.models import Count
from django.db.models import Sum
from demo.models import Demo


@login_required(login_url='/login/')
def dashboard(request):
    ctx = {}
    date_from = datetime.today().date() - timedelta(days=30)
    date_to  = datetime.today().date() + timedelta(days=1)

    ctx['date_from']=str(date_from)
    ctx['date_to']=str(datetime.today().date())

    delta_d = date_to - date_from
    ctx['delta_d'] = delta_d.days    

    enq_list_date = []
    enq_list_count = []

    enroll_list_date = []
    enroll_list_count = []

    followups_list_date = []
    followups_list_count = []

    installments_list_date = []
    installments_list_count = []

    batch_list_date = []
    batch_list_count = []

    demo_list_date = []
    demo_list_count = []

    for i in range(delta_d.days):
        enq_data_date = date_from + timedelta(days=int(i))
        
        enq_obj = Enquiries.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        dm = enq_data_date.strftime("%d %b")
        count = enq_obj.count()
        enq_list_date.append(dm)
        enq_list_count.append(count)

        enq_obj = Enrollments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        enroll_dm = enq_data_date.strftime("%d %b")
        enroll_count = enq_obj.count()
        enroll_list_date.append(enroll_dm)
        enroll_list_count.append(enroll_count)

        followups_obj = Followups.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        followups_dm = enq_data_date.strftime("%d %b")
        followups_count = followups_obj.count()
        followups_list_date.append(followups_dm)
        followups_list_count.append(followups_count)

        installments_discussed_fee_obj = Installments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1),paid_unpaid=True)
        installments_dm = enq_data_date.strftime("%d %b")
        installments_sum = installments_discussed_fee_obj.aggregate(Sum('installment'))
        installments_list_date.append(installments_dm)
        installments_sum = installments_sum['installment__sum']

        
        if not installments_sum:
            installments_sum = 0
        installments_list_count.append(installments_sum)

        batch_obj = Batches.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        batch_dm = enq_data_date.strftime("%d %b")
        batch_count = batch_obj.count()
        batch_list_date.append(batch_dm)
        batch_list_count.append(batch_count)

        demo_obj = Demo.objects.filter(create_on__gte = enq_data_date, create_on__lt= enq_data_date + timedelta(days=1))
        demo_dm = enq_data_date.strftime("%d %b")
        demo_count = demo_obj.count()
        demo_list_date.append(demo_dm)
        demo_list_count.append(demo_count)


    
    ctx['enq_list_date']=enq_list_date
    ctx['enq_list_count']=enq_list_count

    ctx['enroll_list_date']=enroll_list_date
    ctx['enroll_list_count']=enroll_list_count

    ctx['followups_list_date']=followups_list_date
    ctx['followups_list_count']=followups_list_count

    ctx['installments_list_date']=installments_list_date
    ctx['installments_list_count']=installments_list_count

    ctx['batch_list_date']=batch_list_date
    ctx['batch_list_count']=batch_list_count

    ctx['demo_list_date']=demo_list_date
    ctx['demo_list_count']=demo_list_count

    # print(demo_list_date)
    # print(demo_list_count)
    
    return render(request, 'website/dashboard.html', ctx)

def all_filter(request):
    ctx={}
    date_from = request.GET.get("from",None)
    date_to  = request.GET.get("to",None)

    ctx['date_from']=date_from
    ctx['date_to']=date_to

    date_to = (datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)).date()
    date_from = datetime.strptime(date_from,"%Y-%m-%d").date()

    delta_d = date_to - date_from
    ctx['delta_d'] = delta_d.days    

    enq_list_date = []
    enq_list_count = []

    enroll_list_date = []
    enroll_list_count = []

    followups_list_date = []
    followups_list_count = []

    installments_list_date = []
    installments_list_count = []

    batch_list_date = []
    batch_list_count = []

    demo_list_date = []
    demo_list_count = []

    for i in range(delta_d.days):
        enq_data_date = date_from + timedelta(days=int(i))
        enq_obj = Enquiries.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        dm = enq_data_date.strftime("%d %b")
        count = enq_obj.count()
        enq_list_date.append(dm)
        enq_list_count.append(count)

        enq_obj = Enrollments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        enroll_dm = enq_data_date.strftime("%d %b")
        enroll_count = enq_obj.count()
        enroll_list_date.append(enroll_dm)
        enroll_list_count.append(enroll_count)

        followups_obj = Followups.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        followups_dm = enq_data_date.strftime("%d %b")
        followups_count = followups_obj.count()
        followups_list_date.append(followups_dm)
        followups_list_count.append(followups_count)

        installments_discussed_fee_obj = Installments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        installments_dm = enq_data_date.strftime("%d %b")
        installments_sum = installments_discussed_fee_obj.aggregate(Sum('installment'))
        installments_sum = installments_sum['installment__sum']
        if not installments_sum:
            installments_sum = 0
        installments_list_date.append(installments_dm)
        installments_list_count.append(installments_sum)

        batch_obj = Batches.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
        batch_dm = enq_data_date.strftime("%d %b")
        batch_count = batch_obj.count()
        batch_list_date.append(batch_dm)
        batch_list_count.append(batch_count)

        demo_obj = Demo.objects.filter(create_on__gte = enq_data_date, create_on__lt= enq_data_date + timedelta(days=1))
        demo_dm = enq_data_date.strftime("%d %b")
        demo_count = demo_obj.count()
        demo_list_date.append(demo_dm)
        demo_list_count.append(demo_count)
    
    ctx['enq_list_date']=enq_list_date
    ctx['enq_list_count']=enq_list_count

    ctx['enroll_list_date']=enroll_list_date
    ctx['enroll_list_count']=enroll_list_count

    ctx['followups_list_date']=followups_list_date
    ctx['followups_list_count']=followups_list_count

    ctx['installments_list_date']=installments_list_date
    ctx['installments_list_count']=installments_list_count

    ctx['batch_list_date']=batch_list_date
    ctx['batch_list_count']=batch_list_count

    ctx['demo_list_date']=demo_list_date
    ctx['demo_list_count']=demo_list_count

    return render(request, 'website/dashboard.html', ctx)

def get_chart_data(request):
    ctx={}
    date_from = request.GET.get("from",None)
    date_to  = request.GET.get("to",None)
    typee = request.GET.get("type",None)
    # print(typee)

    ctx['date_from']=date_from
    ctx['date_to']=date_to

    date_to = (datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)).date()

    date_from = datetime.strptime(date_from,"%Y-%m-%d").date()

    delta_d = date_to - date_from
    ctx['delta_d'] = delta_d.days
    
    list_date = []
    list_count = []

    for i in range(delta_d.days):
        enq_data_date = date_from + timedelta(days=int(i))

        if typee =="Enquiries":
            enq_obj = Enquiries.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            dm = enq_data_date.strftime("%d %b")
            count = enq_obj.count()
            list_date.append(dm)
            list_count.append(count)
        elif typee == "Enrollments":
            enq_obj = Enrollments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            enroll_dm = enq_data_date.strftime("%d %b")
            enroll_count = enq_obj.count()
            list_date.append(enroll_dm)
            list_count.append(enroll_count)
        elif typee == "Followups":
            followups_obj = Followups.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            followups_dm = enq_data_date.strftime("%d %b")
            followups_count = followups_obj.count()
            list_date.append(followups_dm)
            list_count.append(followups_count)
        elif typee == "Fees Collection":
            installments_discussed_fee_obj = Installments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            installments_dm = enq_data_date.strftime("%d %b")
            installments_sum = installments_discussed_fee_obj.aggregate(Sum('installment'))
            installments_sum = installments_sum['installment__sum']
            if not installments_sum:
                installments_sum = 0
            list_date.append(installments_dm)
            list_count.append(installments_sum)
        elif typee =="Batch":
            batch_obj = Batches.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            batch_dm = enq_data_date.strftime("%d %b")
            batch_count = batch_obj.count()
            list_date.append(batch_dm)
            list_count.append(batch_count)
        elif typee =="Demo":
            demo_obj = Demo.objects.filter(create_on__gte = enq_data_date, create_on__lt= enq_data_date + timedelta(days=1))
            demo_dm = enq_data_date.strftime("%d %b")
            demo_count = demo_obj.count()
            list_date.append(demo_dm)
            list_count.append(demo_count)


    ctx['list_date']=list_date
    ctx['list_count']=list_count
    ctx['type'] = typee
    # print(list_date)
    # print(list_count)
    return render(request, 'website/zoom_chart_data.html',ctx)

def get_zoom_chart_data(request):
    ctx={}

    ctx={}
    date_from = request.GET.get("zfrom",None)
    date_to  = request.GET.get("zto",None)
    typee = request.GET.get("type",None)

    ctx['date_from']=date_from
    ctx['date_to']=date_to

    date_to = (datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)).date()

    date_from = datetime.strptime(date_from,"%Y-%m-%d").date()

    delta_d = date_to - date_from
    ctx['delta_d'] = delta_d.days

    list_date = []
    list_count = []

    for i in range(delta_d.days):
        enq_data_date = date_from + timedelta(days=int(i))

        if typee =="Enquiries":
            enq_obj = Enquiries.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            dm = enq_data_date.strftime("%d %b")
            count = enq_obj.count()
            list_date.append(dm)
            list_count.append(count)
        elif typee == "Enroll":
            enq_obj = Enrollments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            enroll_dm = enq_data_date.strftime("%d %b")
            enroll_count = enq_obj.count()
            list_date.append(enroll_dm)
            list_count.append(enroll_count)
        elif typee == "Followups":
            followups_obj = Followups.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            followups_dm = enq_data_date.strftime("%d %b")
            followups_count = followups_obj.count()
            list_date.append(followups_dm)
            list_date.append(followups_count)
        elif typee == "Fees Collection":
            installments_discussed_fee_obj = Installments.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            installments_dm = enq_data_date.strftime("%d %b")
            installments_sum = installments_discussed_fee_obj.aggregate(Sum('installment'))
            installments_sum = installments_sum['installment__sum']
            if not installments_sum:
                installments_sum = 0
            list_date.append(installments_dm)
            list_count.append(installments_sum)
        elif typee =="Batch":
            batch_obj = Batches.objects.filter(added_on__gte = enq_data_date, added_on__lt= enq_data_date + timedelta(days=1))
            batch_dm = enq_data_date.strftime("%d %b")
            batch_count = batch_obj.count()
            list_date.append(batch_dm)
            list_count.append(batch_count)
        elif typee =="Demo":
            demo_obj = Demo.objects.filter(create_on__gte = enq_data_date, create_on__lt= enq_data_date + timedelta(days=1))
            demo_dm = enq_data_date.strftime("%d %b")
            demo_count = demo_obj.count()
            list_date.append(demo_dm)
            list_count.append(demo_count)


    ctx['list_date']=list_date
    ctx['list_count']=list_count
    ctx['type'] = typee
    return render(request,'website/rezoom_chart_data.html',ctx)