from celery import shared_task
from time import sleep
import os
import csv
import json
from django.template.loader import render_to_string
import requests
from django.conf import settings
from requests.api import request

from instructors.models import Instructors
from .mail_ses import send_mail_ses
# from promotions.models import Campaign
from core.views import get_promotion_data,mark_complete_promotion_send_email_sms,get_bulk_email_data,save_bulk_email_data
from django.core.files.storage import default_storage
# from promotions.models import SendBulkMail
from batches.models import Batches,UnsubscribeBatchReminderEmail


@shared_task
def celfir(timecap):
    sleep(timecap)
    return None


@shared_task
def send_mail(request_id):
    request_obj = get_promotion_data(request_id)
    email_list = []
    csv_path = os.path.join(settings.MEDIA_ROOT,str(request_obj.location))
    with open(csv_path , 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            email_list.append(row[0])

    message_template = request_obj.campaign_template.template_text
    json_data = request_obj.variable_json
    json_data = json.loads(json_data)
    if json_data:
        complete_message = message_template.format(**json_data)
    else:
        complete_message = message_template
    # print(complete_message)
    import html
    complete_message = html.unescape(complete_message)
    # print(type(complete_message))
    # complete_message=render_to_string(complete_message)

    for i in email_list:
        header1 = 'AP2V Offer'
        header12_line = "Promotional Course Offers"
        i = i.strip()
        send_mail_ses(str(i),complete_message,header1,header12_line)
    print("************************************All Mail Sended, Celery Process Completed.****************************************")
    mark_complete_promotion_send_email_sms(request_id)

    return None


@shared_task
def send_sms(request_id):
    request_obj = get_promotion_data(request_id)
    number_list = []
    csv_path = os.path.join(settings.MEDIA_ROOT,str(request_obj.location))
    with open(csv_path , 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            number_list.append(row[0])

    message_template = request_obj.campaign_template.template_text
    json_data = request_obj.variable_json
    json_data = json.loads(json_data)
    complete_message = message_template.format(**json_data)
    # print(complete_message)
    import html
    complete_message = html.unescape(complete_message)
    # print(type(complete_message))
    # complete_message=render_to_string(complete_message)

    for i in number_list:
        url = "https://www.fast2sms.com/dev/bulkV2"
        querystring = {"authorization":settings.FAST2SMS_AUTHORIZATION_KEY,"sender_id":settings.FAST2SMS_SENDER_ID,"message":complete_message,"route":"v3","numbers":i}
        headers = {
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        print("SMS Send to : ")
        print(i)
    print("************************************All SMS Sended, Celery Process Completed.****************************************")
    mark_complete_promotion_send_email_sms(request_id)
    return None

@shared_task
def send_bulk_emails(request_id):
    request_obj = get_bulk_email_data(request_id)
    email_list = []
    csv_path = os.path.join(settings.MEDIA_ROOT,str(request_obj.location))
    with open(csv_path , 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if "@" in row[0]:
                email_list.append(row[0])

    id = request_id
    template_type = request_obj.template_name+str(".html")

    emails_send_response = []

    data = {}
    template_name = "email_templates/"+str(template_type)
    html_content=render_to_string(template_name, data)
    text_content=html_content

    for i in email_list:
        temp_res = {}
        header1 = 'AP2V Offer'
        header12_line = "Promotional Course Offers"
        i = i.strip()
        res,e = send_mail_ses(str(i),text_content,header1,header12_line)
        if res == 1:
            status = "Success"
            temp_res[i]=status
        else:
            status = "Failed-("+str(e)+str(")")
            temp_res[i]=status
        
        emails_send_response.append(temp_res)
    
    print("------------------------Email Send Complete ----------------------------------")

    save_bulk_email_data(request_id,emails_send_response)
    
    return None

@shared_task
def send_batch_reminder_email(batch_id):
    from datetime import timedelta
    data = {}
    email_list = []
    batch_obj = Batches.objects.filter(id = batch_id).first()
    if batch_obj:
        course_list = []
        for j in batch_obj.courses.all():
            course_list.append(j.name)
        
        course_name = " and ".join(course_list)
        batch_start_date = (batch_obj.start_date_time + timedelta(hours=5,minutes=30)).time()

        data['course_name']=course_name
        data['batch_start_date']=batch_start_date
        data['id']=batch_obj.id

        instructor_mail = batch_obj.instructors.email
        #email_list.append(instructor_mail)

        bt = batch_obj.enroll_student.all()
        for k in bt:
            print(k.enquiry_course_id.enquiry_id.email)
            student_email = k.enquiry_course_id.enquiry_id.email
            if "@" in student_email:
                email_list.append(student_email)

        data['all_user']=email_list
        # template_name = "email_templates/"+str(template_type)
        html_content=render_to_string('email/batch_reminder.html', data)
        text_content=html_content

        email_list.append('neeraj@goognu.com')
        email_list.append('amrita@ap2v.com')
        # nr = 1
        for i in email_list:
            exclude_email_obj = UnsubscribeBatchReminderEmail.objects.filter(email=i)
            if not exclude_email_obj:
                # if nr == 1:
                # i = "neeraj@goognu.com"
                temp_res = {}
                header1 = 'Batch Reminder'
                header12_line = "Join your live class."
                i = i.strip()
                res,e = send_mail_ses(str(i),text_content,header1,header12_line)
                # nr = nr+1
            else:
                print("Reminder service Unsubscribed for: ",i)
        
        print("------------------------Email Send Complete ----------------------------------")    
        return None


@shared_task
def send_batch_off_email(batch_id,date):
    from datetime import timedelta
    data = {}
    email_list = []
    batch_obj = Batches.objects.filter(id = batch_id).first()
    if batch_obj:
        course_list = []
        for j in batch_obj.courses.all():
            course_list.append(j.name)
        
        course_name = " and ".join(course_list)
        batch_start_date = (batch_obj.start_date_time + timedelta(hours=5,minutes=30)).time()

        data['course_name']=course_name
        data['batch_start_date']=batch_start_date
        data['id']=batch_obj.id
        data['date']=date
        data['instructore_name'] = batch_obj.instructors.full_name

        instructor_mail = batch_obj.instructors.email
        #email_list.append(instructor_mail)

        bt = batch_obj.enroll_student.all()
        for k in bt:
            print(k.enquiry_course_id.enquiry_id.email)
            student_email = k.enquiry_course_id.enquiry_id.email
            if "@" in student_email:
                email_list.append(student_email)

        data['all_user']=email_list
        # template_name = "email_templates/"+str(template_type)
        html_content=render_to_string('email/batch_off_reminder.html', data)
        text_content=html_content

        email_list.append('neeraj@goognu.com')
        # email_list.append('amrita@ap2v.com')
        # nr = 1
        for i in email_list:
            # exclude_email_obj = UnsubscribeBatchReminderEmail.objects.filter(email=i)
            # if not exclude_email_obj:
                # if nr == 1:
                # i = "neeraj@goognu.com"
            temp_res = {}
            header1 = 'Batch Cancellation'
            header12_line = str("BATCH CANCELLATION on {} ".format(date))
            i = i.strip()
            res,e = send_mail_ses(str(i),text_content,header1,header12_line)
                # nr = nr+1
            # else:
            #     print("Reminder service Unsubscribed for: ",i)
        
        print("------------------------Email Send Complete ----------------------------------")    
        return None

@shared_task
def sending_holiday_notification(holiday_date,ocassion):
    from datetime import datetime
    data={}
    print("---------------------------------------- Sending Email by Celery Start ----------------------------------------")
    # print(ocassion)
    # print(holiday_date)

    student_email_list = []
    batch_obj = Batches.objects.filter(end_date_time__lte = datetime.now().date())
    # print(batch_obj)

    for i in batch_obj:
        bt = i.enroll_student.all()
        for k in bt:
            # print(k.enquiry_course_id.enquiry_id.email)
            student_email = k.enquiry_course_id.enquiry_id.email
            if "@" in student_email:
                if not student_email in student_email_list:
                    student_email_list.append(student_email)
    
    # print(student_email_list)

    data['holiday_date'] = holiday_date
    data['ocassion'] = ocassion

    html_content=render_to_string('email/batch_public_holiday.html', data)
    text_content=html_content

    for i in student_email_list:
        temp_res = {}
        header1 = 'Batch Holiday'
        header12_line = str("Batch Holiday on {} ".format(holiday_date))
        i = i.strip()
        res,e = send_mail_ses(str(i),text_content,header1,header12_line)
        break
    
    print("------------------------Email Send Complete ----------------------------------")    
    return None