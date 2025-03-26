from django.shortcuts import render,redirect
from .customcode import authenticate
from django.contrib.auth import login as auth_login
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
# from django.contrib.auth.models import User
from .models import CustomUserModel, UserRegistrationVerification,UserPasswordResetVerification
from django.contrib.auth import logout as dj_logout
# from users.models import Users
from activity.views import log_activity
from anquira_v2 import choices
import datetime
from enquiries.models import Enquiries
import uuid
import secrets
from django.conf import settings
import random
from django.core.mail import EmailMessage
from communication.views import send_activation_email,send_reset_password_email
from django.views.decorators.csrf import csrf_exempt

def login(request):
    context = {}
    context['user'] = request.user
    names = CustomUserModel.objects.all()
    if request.user.is_authenticated:
        if request.user == "admin":
            dj_logout(request)
            return HttpResponseRedirect('/')
        else:
            if request.user.is_active:
                return HttpResponseRedirect("/dashboard/", context)
            else:
                logout(request)
                return HttpResponseRedirect("/")
    else:
        return render(request, 'users/users_form.html', {'names': names})


def users(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        check_login = authenticate(username=email, password = password)
        if check_login is not None:
            # if check_login.is_active and check_login.user_type=="counselor":
            if check_login.is_active:
                auth_login(request, check_login)
                try:
                    log_activity(request,action=choices.Action.login, action_detail=choices.ActionDetails.login)
                except Exception as e:
                    print(e)    
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

def logout(request):
    for i in request.session.keys():
        try:
            log_activity(request,action=choices.Action.logout, action_detail=choices.ActionDetails.logout)
        except Exception as e:
            print(e)
        del request.session[i]

        try:
            session_keys = list(request.session['enquiry_filter_data'].keys())
            for key in session_keys:
                del request.session['enquiry_filter_data'][key]
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/")



@login_required(login_url = '/')
def edit_profile(request):
    ctx = {}
    ctx['user']=request.user
    if request.method == "POST":
        existing_password = request.POST.get("existing_password")
        new_password = request.POST.get("new_password")
        new_password2 = request.POST.get("new_password2")
        name = request.POST.get('name',False)
        mobile = request.POST.get('mobile',False)
        user = request.user
                   
        
        if name or mobile:
            if name:
                user.first_name=name
            if mobile:
                user.mobile=mobile
            user.save()
            message=False
            status,ctx['profile_message'] = True,"Updated successfully."   

        elif existing_password and new_password and new_password2:
            if request.user.check_password(existing_password):
                if new_password == new_password2:
                    user.set_password(new_password)
                    user.save()
                    status,message = True,"Updated successfully."    
                else:
                    status,message = False,"Reconfirmed password do not match."    
            else:
                status,message = False,"Existing password do not match."    
        else:
            status,message = False,"Some Fields are required"
        ctx['status']=status
        ctx['message'] = message
    return render(request, 'users/edit-profile.html', ctx)


"""
def enquir_reshuffle(request):
    date_before =  datetime.datetime(2021, 8, 10)
    exclude_owner = [] #kirti
    id_skip = []        #skip enquires id in this list.
    enq_obj = Enquiries.objects.filter(added_on__lte = date_before).exclude(reference="Marketing Agency").exclude(assigned_by__first_name__in=exclude_owner).exclude(id__in=id_skip)
    print("Total:", enq_obj.count())

    for i in enq_obj:
        print(i.assigned_by)
    print("---------------------------------")

    n = 1
    new_owner_id = [25,26]
    
    for i in enq_obj:
        if n%2==0:
            Enquiries.objects.filter(id=i.id).update(
                assigned_by=User.objects.get(id=new_owner_id[0])
            )
        else:
            Enquiries.objects.filter(id=i.id).update(
                assigned_by=User.objects.get(id=new_owner_id[1])
            )
        n=n+1
    
    for i in enq_obj:
        print(i.assigned_by)
    print("---------------------------------")
    return HttpResponse(enq_obj)
"""

@csrf_exempt
def create_user(request):
    data={}
    name = request.POST.get("name",None)
    email = request.POST.get("email",None)
    password = request.POST.get("password",None)

    if CustomUserModel.objects.filter(email = email).exists():
        data['code'] = 401
        data['message'] = "This email is already registered with us."
        return JsonResponse(data)
    else:
        token = hex(random.randint(1000000,9999999)).lstrip("0x").rstrip("L")
        uuid_gen = uuid.uuid4().hex

        if UserRegistrationVerification.objects.filter(email = email).exists():
            UserRegistrationVerification.objects.filter(email=email).update(
                uuid = uuid_gen
            )
            token = UserRegistrationVerification.objects.filter(email = email).first().token
            print("TOKEN",token)
        else:
            x = UserRegistrationVerification(
                email = email.lower(),
                name = name,
                password = password,
                token = token,
                uuid = uuid_gen
            )
            x.save()
        
        link = settings.BASE_URL+"/user/activate/"+token+"/"+uuid_gen
        print("LINk",link)
        message = "Hi, "+name+", Your Activateion link is : "+str(link)
        # enquiry_mail_obj = EmailMessage('Account Verification', message, settings.EMAIL_HOST_USER, [email])
        # enquiry_mail_obj.send()
        get_status = send_activation_email(request,name,link,email)
        data['code'] = 200
        data['message'] = "We have sent a verification link, Please verify your email."
        return JsonResponse(data)
    return JsonResponse(data)
        

def activate(request,token,uuid_gen):

    user_reg_obj = UserRegistrationVerification.objects.filter(token=token).first()
    if not user_reg_obj:
        return render(request,'v4_home/email_link_error.html')
    if user_reg_obj.uuid == uuid_gen:
        # username = user_reg_obj.email.split("@")
        username = user_reg_obj.email.replace("@",'.')
        x = CustomUserModel(
            first_name = user_reg_obj.name,
            email = user_reg_obj.email,
            username = username,
            user_type = 'student',
        )
        x.set_password(user_reg_obj.password)
        x.save()

        UserRegistrationVerification.objects.filter(token=token).delete()
    else:
        return render(request,'v4_home/email_link_error.html')
    return redirect('/')


def genrate_reset_user_password_token(request):
    data={}
    if request.method == "POST":
        email = request.POST.get("email",None)
        if email:
            if CustomUserModel.objects.filter(email = email).exists():
                token = hex(random.randint(1000000,9999999)).lstrip("0x").rstrip("L")
                uuid_gen = uuid.uuid4().hex

                if UserPasswordResetVerification.objects.filter(email = email).exists():
                    UserPasswordResetVerification.objects.filter(email=email).update(
                        uuid = uuid_gen
                    )
                    token = UserPasswordResetVerification.objects.filter(email = email).first().token
                else:
                    x = UserPasswordResetVerification(
                        email = email,
                        token = token,
                        uuid = uuid_gen
                    )
                    x.save()
                
                link = settings.BASE_URL+"/user/reset/"+token+"/"+uuid_gen
                user_obj = CustomUserModel.objects.filter(email = email).first()
                get_status = send_reset_password_email(request,user_obj.first_name,link,email)
                data['code'] = 200
                data['message'] = "Please check your email, We have sent a verification link."
                data['status']=200
            else:
                data['message'] = "Email is not registered with us, please sign up."
                data['status'] = 400
        else:
            data['message'] = "Please enter a email."
            data['status'] = 400
    else:
        data['status'] = 400
    return JsonResponse(data)

def reset_password(request):
    if request.method == "POST":
        ctx={}
        password = request.POST.get("password2",None)
        email = request.POST.get("email",None)
        if password and email:
            user_obj = CustomUserModel.objects.filter(email = email).first()
            if user_obj:
                user_obj.set_password(password)
                user_obj.save()
                UserPasswordResetVerification.objects.filter(email=email).delete()
                return redirect("/")
        else:
            ctx['message'] = "Something is wrong, Please try again later after some time."
            return render(request,'v4_home/reset_password.html',ctx)
    return render(request,'v4_home/email_link_error.html')


def reset_password_link_validate(request,token=None, uuid_gen=None):
    ctx={}
    user_reg_obj = UserPasswordResetVerification.objects.filter(token=token).first()
    if not user_reg_obj:
        return render(request,'v4_home/email_link_error.html')
    if user_reg_obj.uuid == uuid_gen:
        ctx['email']=user_reg_obj.email
        return render(request,'v4_home/reset_password.html',ctx)
    else:
        return render(request,'v4_home/email_link_error.html')

def genrate_verification_token(request,name=None,email=None,password=None):

    if name and email and password:
        token = hex(random.randint(1000000,9999999)).lstrip("0x").rstrip("L")
        uuid_gen = uuid.uuid4().hex

        if UserRegistrationVerification.objects.filter(email = email).exists():
            UserRegistrationVerification.objects.filter(email=email).update(
                uuid = uuid_gen
            )
            token = UserRegistrationVerification.objects.filter(email = email).first().token
        else:
            x = UserRegistrationVerification(
                email = email.lower(),
                name = name,
                password = password,
                token = token,
                uuid = uuid_gen
            )
            x.save()
        
        link = settings.BASE_URL+"/user/verify/"+token+"/"+uuid_gen
        print(link)
        message = "Hi, "+name+", Your Activateion link is : "+str(link)
        get_status = send_activation_email(request,name,link,email)
        return 200
    return 400

def auto_reg_activate(request,token,uuid_gen):
    user_reg_obj = UserRegistrationVerification.objects.filter(token=token).first()
    if not user_reg_obj:
        return render(request,'v4_home/email_link_error.html')
    if user_reg_obj.uuid == uuid_gen:
        username = user_reg_obj.email.split("@")
        x = CustomUserModel.objects.filter(email=user_reg_obj.email).update(
            is_verified = True
        )
        UserRegistrationVerification.objects.filter(token=token).delete()
    else:
        return render(request,'v4_home/email_link_error.html')
    return redirect('/')