from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from enquiries.models import Followups,Enquiries,StudentResponse,EnquiryCourses
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import datetime as dt
from datetime import timedelta,datetime
from .filters import FollowupFilter
from anquira_v2.anquira_handlers import ReferenceModeChoices
from courses.models import Courses
from users.models import CustomUserModel
from courses.models import Courses
from anquira_v2.decorators import custome_check
import csv

@login_required(login_url="/")
@custome_check()
def followup_add_details(request):
    if request.method == "GET":
        enquiry_id = request.GET['enquiry_id']
        filter_data = []
        followups_filter_data = Followups.objects.filter(followupid__id = int(enquiry_id)).order_by('-id')
        for i in followups_filter_data:
            data = {
                "enquiry_id": enquiry_id,
                "followups_id": i.id,
                "followup_mode": i.followup_mode,
                "response": i.response,
                "next_followup": i.next_followup.strftime("%a, %d %B %Y"),
                "comments": i.comments,
                "added_on": i.added_on.strftime("%a, %d %B %Y")
            }
            filter_data.append(data)
        return JsonResponse(filter_data, status=200, safe=False)

@login_required(login_url="/")
@custome_check()
def followup_add_accrodion(request, enquiry_id, followups_id):
    if request.method == "POST":
        followups_mode_var = request.POST['followups_mode']
        response_var = request.POST['response']
        next_followup_var = request.POST['next_followup']
        comment_var = request.POST['comment']
        try:
            last_followup_data = Followups.objects.get(id = int(followups_id))
            last_followup_data.status = True
            last_followup_data.save()
            Followups.objects.create(followupid_id = enquiry_id, followup_mode = followups_mode_var, response = response_var, next_followup = next_followup_var, comments = comment_var)
            return JsonResponse({"result": True}, status=200)
        except Exception as e:
            return JsonResponse({"result": False}, status=444)


def _add_one_day(date_str):
    f='%Y-%m-%d'
    d= datetime.strptime(date_str, f)
    d= d + timedelta(days=1)
    return d.strftime(f)

@login_required(login_url = "/")
@custome_check()
def showFollowups(request):
    context_data={}
    request_data  = request.GET.copy()

    if request.user.is_superuser or request.GET.get('o','') =='all':
        pass
    else:
        owner = request.GET.get('owner',request.user.id)
        request_data['owner'] = owner
    q_references=request.GET.getlist('reference')
    request_data['reference'] = ','.join(q_references)
    context_data['q_references'] = q_references

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = '2010-01-01'
    request_data['start_date'] = start_date
    
    end_date=request.GET.get('end_date')
    if not end_date:
        end_date='2030-01-01'
    date_str = end_date
    request_data['end_date']=_add_one_day(date_str)
    is_completed = False
    if request.GET.get('is_completed'):
        is_completed = True

    discarded = False
    if request.GET.get('discarded'):
        discarded = True
    q_courses=request.GET.getlist('course')
    request_data['course'] = ','.join(q_courses)
    context_data['q_courses'] = list(map(int, q_courses))
    
    if request.GET.get('d',False):
        d=request.GET.get('d')
        if d=="pending":
            request_data['start_date'] = datetime.today().strftime('%Y-%m-%d')
            request_data['end_date'] = (datetime.today()+ timedelta(days=1)).strftime('%Y-%m-%d')
        elif d=="overdue":
            #@@request_data['start_date'] = "2020-01-01"
            request_data['end_date'] = datetime.today().strftime('%Y-%m-%d')
        elif d=="tomorrow":
            request_data['start_date'] = (datetime.today()+ timedelta(days=1)).strftime('%Y-%m-%d')
            request_data['end_date'] = (datetime.today()+ timedelta(days=2)).strftime('%Y-%m-%d')
    if discarded and is_completed:
        followups = Followups.objects.all().order_by("-next_followup")
    elif discarded and not is_completed:
        followups = Followups.objects.all().order_by("-next_followup")
    elif is_completed and not discarded:
        followups = Followups.objects.filter(followupid__discard=False).order_by("-next_followup")
    else:
        followups = Followups.objects.all().order_by("-next_followup")

    
    if request.GET.get('o',False):
        o=request.GET.get('o')
        if o=="my":
            followups = followups.filter(assigned_user=request.user)

    # no_status_enquiries=Enquiries.objects.filter(enquirycourses__status=EnquiryCourses.NONE).values_list('id').distinct()
    # followups = followups.filter(followupid__in=no_status_enquiries,is_complete=False).order_by('next_followup')
    
    followups = FollowupFilter(request_data, queryset=followups).qs
    fid =[]
    for i in followups:
        fi=i.id
        fid.append(fi)
    print("followups: ",followups)    
    context_data["fid"]= fid
    page = request.GET.get('page', 1)
    p = Paginator(followups,25, request=request)
    data= p.page(page)
    # print("data: ",data)
    context_data["Followups"]= data
    context_data['references']= ReferenceModeChoices.choice
    context_data['courses'] = Courses.objects.all().order_by('name')
    context_data['locations'] = Enquiries.BRANCH_LOCATION
    context_data['users'] = CustomUserModel.objects.filter(exist_employee=True)
    context_data['student_responses'] = StudentResponse.objects.all().order_by('priority')
    context_data['page_obj'] = data
    # context_data['eid'] = list(eid)
    
    return render(request, 'list_followups.html', context_data)


def followupsCSV(request):
    # print(request.body)
    context_data={}
    enroll_id = request.GET.get("followups_id",None)
    # print('pooppo'*100)
    # print(enroll_id)
    # print(type(enroll_id))

    enroll_id = enroll_id.replace('[','')
    enroll_id = enroll_id.replace(']','')
    enroll_id = enroll_id.split(",")
    enroll_id = [int(i) for i in enroll_id]

    enrollments_obj = Followups.objects.filter(id__in=list(enroll_id))
    
    # print(enrollments_obj)
    # print(enrollments_obj.count())

    
    enrollments = []
    for e_obj in enrollments_obj:
        values = {
                    'id': e_obj.id,
                    'full_name': e_obj.followupid.full_name,
                    'mobile': e_obj.followupid.mobile,
                    'email': e_obj.followupid.email,
                }
        
        enrollments.append(values)
    context_data ={"enrollments": enrollments}

    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['SrNo','Id','name','mobile','email'])

    n = 1
    for i in enrollments:
    
        row = (
            n,
            i['id'],
            i['full_name'],
            i['mobile'],
            i['email'],
           
        )
        n=n+1
        writer.writerow(row)

    response['Content-Disposition'] = 'attachment; filename=FollowupsData-{date}.csv'.format(date=datetime.now().strftime('%d-%m-%Y'),)
    return response
    # return HttpResponse("ok")