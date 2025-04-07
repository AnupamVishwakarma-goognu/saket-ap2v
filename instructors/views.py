import email
import sre_compile
from django.conf import settings
from django.shortcuts import redirect, render

from bluejeans.zoom import create_zoom_user
from .models import Instructors
from courses.models import Courses
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from anquira_v2.anquira_handlers import (
    DayOfWeekChoices
)
from .filters import (
    InstructorsFilter
)

from django.core.paginator import Paginator
from activity.views import log_activity
from anquira_v2 import choices
from bluejeans.views import create_user_instructor,activate_user_room
import secrets
from users.models import CustomUserModel as User
import random
from anquira_v2.decorators import custome_check
from batches.models import Batches
from communication.models import CounselorContactNumber
from enrolls.models import Enrollments
import datetime

@login_required(login_url = '/')
@custome_check()
def instructor(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        courses = request.POST.getlist('course[]')
        weekdays = ",".join(request.POST.getlist('weekDays[]'))
        # added_on = request.POST['added_on']

        if Instructors.objects.filter(email=email).exists() :
            return JsonResponse({"result": False}, status=444)

        try:
            created_instructor = Instructors.objects.create(full_name=full_name, email=email, mobile=mobile, days_of_week = weekdays)
            try:
                log_activity(request,action=choices.Action.add_instructor, action_detail=choices.ActionDetails.add_instructor,id=created_instructor.id)
            except Exception as e:
                print(e)
            password_length = 5
            x = User(
                first_name = full_name,
                email = email,
                mobile = mobile,
                username = email,
                user_type = 'instructor',
            )
            x.set_password(str(email)+str(mobile))
            x.save()

            for i in courses:
                created_instructor.courses.add(int(i))
            return JsonResponse({"result": True,"password":str(email)+str(mobile)}, status=200)
        except Exception as e:
            print("error in instructor views:",e)
            return JsonResponse({"result": False}, status=444)
    context_data = {
        'course': Courses.objects.all().order_by('name'),
        'InstructorsWeekDays': Instructors,
    }
    return render(request, 'instructors/instructor_form.html', context_data)

@login_required(login_url="/")
@custome_check()
def instructorview(request, instructors_id):
    instructor = Instructors.objects.get(id = instructors_id)
    courses = Courses.objects.all().order_by('name')
    all_courses = []
    added_courses = [i.name for i in instructor.courses.get_queryset()]
    for course in courses:
        if course.name in added_courses:
            all_courses.append({'name': course.name, 'id': course.id, 'status': True})
        else:
            all_courses.append({'name': course.name, 'id': course.id, 'status': False})

    working_days = instructor.days_of_week.split(',')
    context_data = {
        'instructor': instructor,
        'courses': courses,
        'all_courses': all_courses,
        'working_days': working_days,
        'days_of_week_all': DayOfWeekChoices.choice
    }
    
    print("----------------------------------------===")
    return render(request, 'instructors/view.html', context_data)

@login_required(login_url="/")
@custome_check()
def instructorlist(request):
    instructors = Instructors.objects.filter(active=True).order_by('-added_on')
    data = request.GET.copy()
    q_weekday=request.GET.getlist('weekday')
    
    
    data['weekday'] = ",".join(q_weekday)
    
    q_courses=request.GET.getlist('course')
    data['course'] = ','.join(q_courses)
    
    instructors = InstructorsFilter(data, instructors).qs

    paginator = Paginator(instructors, 10)
    page_number = request.GET.get('page')
    try:
        instructors = paginator.page(page_number)
    except:
        instructors = paginator.page(1)

    context_data = {
        'instructor': instructors,
        'courses': Courses.objects.all().order_by('name'),
        'weekdays':Instructors.WEEKDAYS_CHOICES,
        'q_weekday':q_weekday,
        'q_courses': list(map(int, q_courses))
    }
    return render(request, 'instructors/list.html', context_data)

@login_required(login_url="/")
@custome_check()
def inactive_instructorlist(request):
    instructors = Instructors.objects.filter(active=False).order_by('-added_on')
    data = request.GET.copy()
    q_weekday=request.GET.getlist('weekday')
    
    
    data['weekday'] = ",".join(q_weekday)
    
    q_courses=request.GET.getlist('course')
    data['course'] = ','.join(q_courses)
    
    instructors = InstructorsFilter(data, instructors).qs

    paginator = Paginator(instructors, 10)
    page_number = request.GET.get('page')
    try:
        instructors = paginator.page(page_number)
    except:
        instructors = paginator.page(1)

    context_data = {
        'instructor': instructors,
        'courses': Courses.objects.all().order_by('name'),
        'weekdays':Instructors.WEEKDAYS_CHOICES,
        'q_weekday':q_weekday,
        'q_courses': list(map(int, q_courses)),
        'inactive' : 'yes'
    }
    return render(request, 'instructors/list.html', context_data)

class InstructorsDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/'
    success_url = reverse_lazy('instructorlist')
    model = Instructors

    def get(self, *args, **kwargs):
        r_dict = {
            'status': None,
        }
        try:
            # self.delete(self.request, *args, **kwargs)
            instructor_id = kwargs['pk']
            Instructors.objects.filter(id=instructor_id).update(
                active = False
            )
            r_dict.update(status=1)

            return JsonResponse(r_dict)
        except:
            r_dict.update(status=0)
            return JsonResponse(r_dict)

class InstructorupdateView(View):
    redirect_url = 'instructorlist'
    model = Instructors

    def post(self, *args, **kwargs):
        instructor_obj = Instructors.objects.filter(
            id=self.kwargs.get('instructor_id')
        )
        if instructor_obj.exists():
            instructor_queryset = Instructors.objects.filter(id=self.kwargs.get('instructor_id')).first()
            if not User.objects.filter(email = self.request.POST.get('email')).exists():
                password_length = 5
                x = User(
                    first_name = self.request.POST.get('fullname'),
                    email = self.request.POST.get('email'),
                    mobile = self.request.POST.get('mobile'),
                    username = self.request.POST.get('email'),
                    user_type = 'instructor',
                )
                x.set_password(str(email)+str(mobile))
                x.save()

            instructor_obj.update(
                full_name=self.request.POST.get('fullname'),
                email=self.request.POST.get('email'),
                mobile=self.request.POST.get('mobile'),
                days_of_week=",".join(self.request.POST.getlist('days_of_week[]')),
            )

            courses = self.request.POST.getlist('courselist[]')
            if courses:
                instructor_obj_loop = instructor_obj.first()
                remove_data=instructor_obj_loop.courses.exclude(id__in=list(map(int, courses)))
                instructor_obj_loop.courses.set(courses)
                
                for p in remove_data:
                    instructor_obj_loop.courses.remove(p.id)

        response_data = {
            'status': 1,
            'redirect': reverse(self.redirect_url)
        }

        ins = self.kwargs.get('instructor_id')
        # print(self.kwargs.get('instructor_id'))
        # print(self.request.user)
        try:
            log_activity(self.request,action=choices.Action.mod_instructor, action_detail=choices.ActionDetails.mod_instructor,id=ins)
        except Exception as e:
            print(e)
        return JsonResponse(response_data)

def get_instructors_course(request):
    ctx={}
    id = request.GET.get("id",None)
    if id:
        inst_obj = Instructors.objects.filter(id=id).first()
        print(inst_obj)
        ctx['inst_obj'] = inst_obj
    return render(request,'instructors/instructor_course.html',ctx)

def mark_as_instructore(request):
    response_data = {}
    inst_id = request.GET.get("inst_id",None)
    if inst_id:
        print(inst_id)

        inst_obj = Instructors.objects.filter(id=inst_id).first()
        if inst_obj:
            full_name = inst_obj.full_name
            created_instructor_id = inst_id

            blue_jeans_user_id = create_user_instructor(request,full_name,created_instructor_id,reactive=True)
            pass_code,json_data = activate_user_room(request,blue_jeans_user_id)
            
            Instructors.objects.filter(id=created_instructor_id).update(
                blue_jeans_user_id=blue_jeans_user_id,blue_jeans_passcode=pass_code,user_room_json=json_data,active=True
            )
            return JsonResponse(response_data,status=200)
        return JsonResponse(response_data,status=404)
    return JsonResponse(response_data,status=404)
        
def genrate_zoom_user(request, user_id):
    import secrets
    print(user_id)
    if user_id:
        int_obj = Instructors.objects.filter(id=user_id).first()
        if int_obj:
            if int_obj.zoom_email:
                print("Exists")
            else:
                print("Not Exists...")

                name = int_obj.full_name
                email = int_obj.email
                # email_split = email.split("@")
                # new_email = email_split[0]+"+"+str(user_id)+"@"+email_split[1]

                password =  secrets.token_urlsafe(10)

                responce_data = create_zoom_user(name,email,password)

                Instructors.objects.filter(id=user_id).update(
                    zoom_email = email,
                    zoom_password = password
                )
    return redirect("/instructors/view/"+str(user_id)+"/")

def use_comman_zoom_user(request, user_id):
    import secrets
    print(user_id)
    if user_id:
        int_obj = Instructors.objects.filter(id=user_id).first()
        if int_obj:
            Instructors.objects.filter(id=user_id).update(
                zoom_email = settings.DEFAULT_INSTRUCTOR_EMAIL,
            )
    return redirect("/instructors/view/"+str(user_id)+"/")

def target_record(request):
    ctx={}

    instructor_id = request.GET.get("instructor",None)
    start_date = request.GET.get("start_date",None)
    end_date = request.GET.get("end_date",None)

    # print(start_date)
    # print(end_date)
    if start_date:
        start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    else:
        # start_date = datetime.datetime.today() - datetime.timedelta(days=30)
        start_date = datetime.datetime.today().replace(day=1)
    
    if end_date:
        end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()

    if instructor_id:
        inst_obj = Instructors.objects.filter(id=instructor_id)
        ctx['inst_id'] = int(instructor_id)
    else:
        inst_obj = Instructors.objects.all()
    ctx['inst_obj'] = Instructors.objects.all()
    
    this_month = datetime.datetime.now().month
    inst_list = []
    for i in inst_obj:
        inst_dict = {}
        fee_sum = 0
        batch_obj = Batches.objects.filter(instructors_id = i.id,start_date_time__gte=start_date,start_date_time__lte=end_date)
        # print(batch_obj)
        for j in batch_obj:
            all_student = j.enroll_student.all()
            for stu in all_student:
                #print(stu.discussed_fee)
                # print(stu.registered_on.month)
                # if stu.registered_on.month == this_month:
                # if start_date and end_date:
                #     reg_date = stu.registered_on
                #     print(reg_date.date())
                #     print(type(reg_date))
                #     if reg_date.date() >= start_date.date() and reg_date.date() <= end_date.date():
                # fee_sum = fee_sum+(stu.discussed_fee*82)/100    #18% = 100-18=82
                fee_sum = fee_sum+(stu.ap2v_share)    #18% = 100-18=82
        print(fee_sum)
        print('neeraj'*100)
        inst_dict['name'] = i.full_name
        inst_dict['fee'] = fee_sum
        inst_list.append(inst_dict)
    
    # print(inst_list)
    ctx['inst_list'] = inst_list
    ctx['start_date'] = start_date.date()
    ctx['end_date'] = end_date.date()
    return render(request, 'instructors/trainer_record.html',ctx)



def counselor_record(request):
    ctx={}
    counselor_id = request.GET.get("counselor",None)
    start_date = request.GET.get("start_date",None)
    end_date = request.GET.get("end_date",None)
    clist=[]
   
    if start_date:
        start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    else:
        # start_date = datetime.datetime.today() - datetime.timedelta(days=30)
        start_date = datetime.datetime.today().replace(day=1)
    
    if end_date:
        end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()
    if counselor_id:
        
        couns_obj= User.objects.filter(id=counselor_id)
        ctx['couns_id'] = int(counselor_id)
    else:
        couns_obj= User.objects.filter(user_type='counselor')
        ctx['couns_obj']=couns_obj
    
    counselor_list=[]
    for j in couns_obj:
        # print('='*100)
        # print(j.id)
        counselor_dict={}
        fee_sum=0
        
        enroll_obj=Enrollments.objects.filter(registered_by_id=j.id,registered_on__gte=start_date,registered_on__lte=end_date)
        for z in enroll_obj:
            fee_sum+=int(z.ap2v_share)            
            print(j.name, fee_sum)
        

        counselor_dict['name'] = j
        counselor_dict['fee'] = fee_sum
        counselor_list.append(counselor_dict)
    
    

    ctx['clist']=clist
    ctx['start_date'] = start_date
    ctx['end_date'] = end_date
    ctx['counselor_list']=counselor_list
    ctx['couns_obj']=User.objects.filter(user_type='counselor')
    
    
    
    return render(request, 'instructors/counselor_record.html', ctx)

def all_couselor_record(request):
    ctx={}
    counselor_id = request.GET.get("cid",None)
    start_date = request.GET.get("start",None)
    end_date = request.GET.get("end",None)
    print('8**'*100)
    print(start_date)
    print(end_date)
    print(counselor_id)

    if start_date:
        start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    else:
        # start_date = datetime.datetime.today() - datetime.timedelta(days=30)
        start_date = datetime.datetime.today().replace(day=1)
    
    if end_date:
        end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    else:
        end_date = datetime.datetime.today()
    couns_obj= User.objects.filter(id=counselor_id).first()
    # ctx['couns_id'] = int(counselor_id)
    # enddate=datetime.datetime.today()
    # startdate=enddate-datetime.timedelta(days=4)
    # print('start date',startdate)
    # print('end date',enddate)
    # print('P'*100)
    print('this is counselor id ',counselor_id)
    enroll_obj=Enrollments.objects.filter(registered_by_id=counselor_id,registered_on__gte=start_date,registered_on__lte=end_date )
    T_amout=0
    current_recive_ap2v=0
    final_amount=0
    for i in enroll_obj:
        print('this is recive',i.ap2v_share_recived)
        final_amount+=i.ap2v_share
        current_recive_ap2v+=i.ap2v_share_recived
        T_amout+=i.discussed_fee
   
    # print('this target amount',T_amout)
    # print('this final target amount',final_amount)
    
    print(enroll_obj)
    ctx['allenroll']=enroll_obj
    ctx['start']=start_date
    ctx['end']=end_date
    ctx['counselor_id']=couns_obj
    ctx['target']=T_amout
    ctx['final_amount']=final_amount
    ctx['current_recive_ap2v']=current_recive_ap2v
    return render(request,'instructors/all_couselor_record.html', ctx)    