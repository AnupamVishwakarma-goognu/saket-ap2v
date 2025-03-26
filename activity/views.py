from django.shortcuts import render
from django.http import HttpResponse
from .models import Activity
from django.core.paginator import Paginator
from anquira_v2 import choices
# from django.contrib.auth.models import User
from users.models import CustomUserModel
from datetime import datetime,time

# Create your views here.

def activity(request):
    ctx={}
    if request.user.is_superuser:
        activity_queryset = Activity.objects.all().order_by('-id')
    else:
        activity_queryset = Activity.objects.filter(user = request.user).order_by('-id')
    
    paginator = Paginator(activity_queryset, 10)
    page_number = request.GET.get('page')

    try:
        activity_queryset = paginator.page(page_number)
    except:
        activity_queryset = paginator.page(1)

    ctx['activity_queryset'] = activity_queryset
    return render(request,'activity/activity_list.html',ctx)

# log_activity()
# log_activity(user = request.user, action = Activity.ACTIONS.add_enquiry, action_ref_id = 10)
# log_activity(user = request.user, action = Activity.ACTIONS.add_followup, action_ref_id = 110)

def log_activity(request=None, action=None, action_detail=None,id=None):
    if action and action_detail:
        """ |*************************************************************|
            |** NoTe : {type is action  AND  ref_type id action_detail} **|
            |*************************************************************|"""
        action_detail = action_detail.replace('%d',str(id))

        x = Activity(
            user = request.user,
            typee = action,
            # ref_type = action_detail,
            ref_id = id
        )
        x.save()
        return x
    return "Error"

def get_enquiry_by_followup(request):
    """
    return redirect(revese()):
    """
    pass


def result(request):
    # print("--------------------------------------------------------------")
    name = request.GET['name']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    mobile = request.GET['mobile']
    email = request.GET['email']
    # print(name)
    # print(start_date)
    # print(end_date)
    # print(mobile)
    # print(email)

    cd = str(datetime.now().date())
    sd = start_date+" 00:00:00"
    ed = end_date+" 11:59:59"

    # sd = datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
    # ed = datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")

    activity_queryset = Activity.objects.filter(user__first_name__contains = name,user__mobile__contains = mobile,user__email__contains = email)
    try:
        if start_date and end_date:
            activity_queryset = activity_queryset.objects.filter(add_on__date__range = (sd,ed))
    except Exception as e:
        print(e)
    # print(activity_queryset)

    ctx={}
    # if request.user.is_superuser:
    #     activity_queryset = Activity.objects.all().order_by('-id')
    # else:
    #     activity_queryset = Activity.objects.filter(user = request.user).order_by('-id')
    
    paginator = Paginator(activity_queryset, 10)
    page_number = request.GET.get('page')

    try:
        activity_queryset = paginator.page(page_number)
    except:
        activity_queryset = paginator.page(1)

    ctx['activity_queryset'] = activity_queryset
    return render(request,'activity/activity_list.html',ctx)