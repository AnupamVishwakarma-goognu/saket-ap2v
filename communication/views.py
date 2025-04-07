from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import csv
import json
import requests
from django.core.files.storage import default_storage
from demo.models import DemoSMSTemplate
from enquiries.models import Enquiries,EnquiryCourses
from .models import CounselorContactNumber
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from .mail_ses import send_mail_ses
from .task import *

# Create your views here.


class SendSMS():
    def send_sms_fast2sms(request):
        # number_list = []
        # csv_path = os.path.join(settings.MEDIA_ROOT,str(request.location))
        # with open(csv_path , 'r') as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         number_list.append(row[0])

        # message_template = request.campaign_template.template_text
        # json_data = request.variable_json
        # json_data = json.loads(json_data)
        # complete_message = message_template.format(**json_data)
        # # complete_message="Hello, This is Text Message"


        # for i in number_list:
        #     url = "https://www.fast2sms.com/dev/bulkV2"
        #     querystring = {"authorization":settings.FAST2SMS_AUTHORIZATION_KEY,"sender_id":settings.FAST2SMS_SENDER_ID,"message":complete_message,"route":"v3","numbers":i}
        #     headers = {
        #         'cache-control': "no-cache"
        #     }
        #     response = requests.request("GET", url, headers=headers, params=querystring)
        #     # print(response.text)

        
        request_id = request.id
        send_sms.delay(request_id)
        return JsonResponse({"data":"pass"},status=200)
    
    def send_demo_batch_sms_fast2sms(request,title,start_date,meeting_link,stu_list,template_id):
        number_list = []
        for i in stu_list:
            stu_data = {}
            enq_obj = Enquiries.objects.get(id = int(i))
            if enq_obj.mobile:
                if enq_obj.full_name:
                    stu_data['name'] = enq_obj.full_name
                else:
                    stu_data['name'] = "student"

                stu_data['mobile'] = enq_obj.mobile
                stu_data['course'] = title
                stu_data['datetime'] = start_date.strftime("%m/%d/%Y, %I:%M %p")
                stu_data['link'] = meeting_link
                number_list.append(stu_data)

        message_template = DemoSMSTemplate.objects.get(id=template_id).template_text
        
        # complete_message="Hello, This is Text Message"


        for i in number_list:
            complete_message = message_template.format(**i)
            number = i['mobile'].lstrip("0")
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {"authorization":settings.FAST2SMS_AUTHORIZATION_KEY,"sender_id":settings.FAST2SMS_SENDER_ID,"message":complete_message,"route":"v3","numbers":number}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        return JsonResponse({"data":"pass"},status=200)

def send_promotional_email(request):
    # send_mail.delay([1,2,3,4,5,6,7,8,9,5,2,5,2,5,2,5,5,2,5])
    request_id = request.id 
    send_mail.delay(request_id)
        # print(response.text)
    return JsonResponse({"data":"pass"},status=200)


def get_number(request):
    number = CounselorContactNumber.objects.filter(used_number=False).first()
    if number is None:
        all_number = CounselorContactNumber.objects.all()
        for i in all_number:
            CounselorContactNumber.objects.filter(id=i.id).update(
                used_number = False
            )
        number = CounselorContactNumber.objects.filter(used_number=False).first()
        CounselorContactNumber.objects.filter(number=number.number).update(
            used_number = True
        )
        return number.number
    else:
        CounselorContactNumber.objects.filter(number=number.number).update(
            used_number = True
        )
        return number.number
    
def send_demo_invite_email(request,title=None,start_date=None,meeting_link=None,stu_list=None):
    # print("------------Sending Mail-------------------")
    
    email_list = []
    for i in stu_list:
        stu_data = {}
        enq_obj = Enquiries.objects.get(id = int(i))
        if enq_obj.email:
            if enq_obj.full_name:
                stu_data['name'] = enq_obj.full_name
            else:
                stu_data['name'] = "student"

            stu_data['email'] = enq_obj.email
            stu_data['course'] = title
            stu_data['datetime'] = start_date.strftime("%m/%d/%Y, %I:%M %p")
            stu_data['link'] = meeting_link
            email_list.append(stu_data)

    for j in email_list:
        data = j
        html_content=render_to_string('email/demo_batch_email.html', data)
        text_content=html_content
        header1 = 'Demo Invitation'
        header12_line = "AP2V Demo Batch"

        send_mail_ses(j['email'],text_content,header1,header12_line)
    return "success"
def send_batch_invite_email(request,title=None,start_date=None,meeting_link=None,stu_list=None):
    
    email_list = []
    for i in stu_list:
        stu_data = {}
        enq_obj =EnquiryCourses.objects.get(id = int(i)).enquiry_id
        if enq_obj.email:
            if enq_obj.full_name:
                stu_data['name'] = enq_obj.full_name
            else:
                stu_data['name'] = "student"

            stu_data['email'] = enq_obj.email
            stu_data['course'] = title
            stu_data['datetime'] = start_date.strftime("%m/%d/%Y, %I:%M %p")
            stu_data['link'] = meeting_link
            email_list.append(stu_data)

    for j in email_list:
        data = j
        html_content=render_to_string('email/batch_email.html', data)
        text_content=html_content

        header1 = title+' Batch Invitation'
        header12_line = "AP2V Batch"

        send_mail_ses(j['email'],text_content,header1,header12_line)
    return "success"

def send_activation_email(request, name=None, link=None,email=None):
    data = {'name':name,'link':link}
    html_content=render_to_string('email/verification_email.html', data)
    text_content=html_content
    header1 = 'Email Verification'
    header12_line = 'AP2V Account Verification'

    send_mail_ses(email,text_content,header1,header12_line)

def send_reset_password_email(request, name=None, link=None,email=None):
    data = {'name':name,'link':link}
    html_content=render_to_string('email/password_reset_email.html', data)
    text_content=html_content

    header1 = 'Reset Password'
    header12_line = 'AP2V Account Verification'

    send_mail_ses(email,text_content,header1,header12_line)

def send_anquira_report_email(data=None):
    data = {'data':data }
    html_content=render_to_string('email/report.html', data)
    text_content=html_content

    email = settings.REPORT_SENT_TO_EMAILS
    today = datetime.today().strftime('%d-%m-%Y')
    email_subject = 'Anquira Daily Report - {}'.format(today)
    # msg = EmailMultiAlternatives(email_subject, text_content, "Anquira Report<"+settings.EMAIL_HOST_USER+">", email)
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Anquira Report'
    header12_line = 'Anquira Daily Report - {}'.format(today)
    for se in email:
        send_mail_ses(se,text_content,header1,header12_line)

def send_refund_email(request, name=None, enrollment=None,amount=None,date=None):
    data = {'name':name,'enrollment':enrollment,'amount':amount,'date':date}
    html_content=render_to_string('email/refund.html', data)
    text_content=html_content

    email = settings.ADMIN_EMAIL
    # msg = EmailMultiAlternatives('Refund Initiated for '+name, text_content, "Refund<"+settings.EMAIL_HOST_USER+">", [email])
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Refund Initiated for '+name
    header12_line = 'Refund'

    send_mail_ses(email,text_content,header1,header12_line)

def send_enrollment_email(request, course_name=None,email=None,password=None):
    data = {'course_name':course_name,"password":password,"email":email}
    html_content=render_to_string('email/enroll_mail.html', data)
    text_content=html_content

    # print(text_content)
    # print(email)

    # msg = EmailMultiAlternatives('Welcome to AP2V - You are successfully Enrolled', text_content, "Enrollment<"+settings.EMAIL_HOST_USER+">", [email])
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Welcome to AP2V - You are successfully Enrolled'
    header12_line = "Enrollment"

    send_mail_ses(email,text_content,header1,header12_line)



def send_recording_urls_count_mail():
    data={}
    html_content=render_to_string('email/recording_urls_count_mail.html', data)
    text_content=html_content

    emails = settings.ADMIN_EMAILS
    # msg = EmailMultiAlternatives('Alert-Recording URL Count...', text_content, "Alert<"+settings.EMAIL_HOST_USER+">", emails)
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Alert-Recording URL Count....'
    header12_line = 'Alert'

    send_mail_ses(emails,text_content,header1,header12_line)


def send_enquiry_resign_mail(enquiry_id,from_counselor, to_counselor):
    data = {'enquiry_id':enquiry_id,'from_counselor':from_counselor,'to_counselor':to_counselor}
    html_content=render_to_string('email/send_reassigned_mail.html', data)
    text_content=html_content

    email = settings.REASSIGN_NOTIFICATION_EMAILS
    # msg = EmailMultiAlternatives('Reassign Enquiry Owner for '+str(enquiry_id), text_content, "Reassign Notification <"+settings.EMAIL_HOST_USER+">", settings.REASSIGN_NOTIFICATION_EMAILS)
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Reassign Enquiry Owner for '+str(enquiry_id)
    header12_line = 'Reassign Notification'

    send_mail_ses(email,text_content,header1,header12_line)


def send_certificate_email(name,link,email,course_name=None):
    data = {'name':name,'link':link,"course_name":course_name}
    html_content=render_to_string('email/send_certificate_email.html', data)
    text_content=html_content
    # email = "neeraj@goognu.com"

    # msg = EmailMultiAlternatives('AP2V Course Certificate ', text_content, "Certificate <"+settings.EMAIL_HOST_USER+">", [email])
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'AP2V Course Certificate'
    header12_line = 'Certificate'

    send_mail_ses(email,text_content,header1,header12_line)

def send_batch_join_alert_email(email=None,course_name=None):
    data = {"course_name":course_name}
    html_content=render_to_string('email/send_batch_alert_email.html', data)
    text_content=html_content
    email = "neeraj@goognu.com"

    # msg = EmailMultiAlternatives('Batch Joining Time ', text_content, "You missed your batch <"+settings.EMAIL_HOST_USER+">", [email])
    # msg.attach_alternative(html_content, "text/html")
    # status=msg.send()

    # ----------------------------------------------------------------------------------------------------------------------------------------------
    header1 = 'Batch Joining Time'
    header12_line = 'You missed your batch'

    send_mail_ses(email,text_content,header1,header12_line)


def send_bulk_email_comm(self):
    send_bulk_emails.delay(self.id)
    return JsonResponse({"data":"pass"},status=200)

def send_batch_reminder(batch_id):
    print(batch_id)
    send_batch_reminder_email.delay(batch_id)

def send_batch_off_reminder(batch_id,date):
    print(batch_id)
    print(date)
    send_batch_off_email.delay(batch_id,date)

def sending_holiday_email(holiday_date,ocassion):
    print(holiday_date)
    print(ocassion)
    sending_holiday_notification.delay(holiday_date,ocassion)