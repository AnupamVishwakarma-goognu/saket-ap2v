from datetime import datetime
from django.shortcuts import redirect, render
from activity.views import log_activity
from communication.views import send_bulk_email_comm
# from anquira import promotions
from anquira_v2 import choices
from .models import Campaign,CampaignTemplate
from django.http import HttpResponse, JsonResponse
import re
import json
from anquira_v2.decorators import custome_check
from django.contrib.auth.decorators import login_required
import os
import csv
import json
import requests
from promotions.models import SendBulkMail
from communication.task import *


@login_required(login_url = '/')
@custome_check()
def list_promotions(request):
    ctx = {}
    campaign = Campaign.objects.all().order_by("-id")
    campaign_template = CampaignTemplate.objects.all()
    ctx['campaign_template']=campaign_template
    ctx['campaign']=campaign
    return render(request, 'promotions/list_promotions.html', ctx)


def add_promotion(request):
    if request.method == "POST":
        variable_field_count = request.POST.get("variable_field_count",None)
        campaign_name = request.POST.get("campaign_name",None)
        campaign_type = request.POST.get("campaign_type",None)
        campaign_source = request.POST.get("campaign_mode",None)
        campaign_template = request.POST.get("campaign_template",None)

        if campaign_type=="sms":
            campaign_message = request.POST.get("sms",None)
        else:
            campaign_message = request.POST.get("ckeditor",None)

        if campaign_source == "csv":
            csv_file = request.FILES['data_file']
        else:
            csv_file = None

        variables_list = re.findall(r'{(.*?)}', CampaignTemplate.objects.filter(id=campaign_template).first().template_text)
        variable_value_json = {}
        if variable_field_count:
            for i in range (1,int(variable_field_count)+1):
                variable_value_json[variables_list[i-1]] = request.POST.get("variable"+str(i),None)

        import json
        variable_value_json = json.dumps(variable_value_json)
        x = Campaign(
            campaign_template = CampaignTemplate.objects.get(id=campaign_template),
            c_type = campaign_type,
            source = campaign_source,
            location = csv_file,
            variable_json=variable_value_json
        )
        x.save()

        # try:
        #     log_activity(request,action=choices.Action.add_promotion, action_detail=choices.ActionDetails.add_promotion,id='0')
        # except Exception as e:
        #     print(e)
    return redirect (list_promotions)


def get_campaign_template(request):
    template_id = request.GET.get('template_id',None)
    data={}
    if template_id:
        template_obj = CampaignTemplate.objects.filter(id=template_id).first()
        data['template_text'] = template_obj.template_text
        data['variable_count'] = template_obj.variable_count
    return JsonResponse(data, status=200) 

def display_campaign_view(request):
    ctx={}
    campaign_id = request.GET.get("campaign_id",None)
    # print(campaign_id)
    if campaign_id:
        campaign_obj = Campaign.objects.filter(id=campaign_id).first()
        ctx['campaign_obj']=campaign_obj

        message_template = campaign_obj.campaign_template.template_text
        json_data = campaign_obj.variable_json
        json_data = json.loads(json_data)
        if json_data:
            complete_message = message_template.format(**json_data)
        else:
            complete_message = message_template
        # print(complete_message)
        ctx['complete_message']=complete_message
        
    return render(request,'promotions/promotion_view.html',ctx)

def get_template_type(request):
    ctx={}
    type_id = request.GET.get('type_id',None)
    if type_id:
        camp_temp_obj = CampaignTemplate.objects.filter(camp_temp_type = type_id)
        ctx['campaign_template']=camp_temp_obj
    return render(request,'promotions/templates.html',ctx)

def send_mails(request):
    ctx={}
    send_obj = SendBulkMail.objects.all()
    ctx['send_obj']=send_obj
    return render(request,'promotions/send_mail.html',ctx)

def check_upload_csv(request):
    data={}
    csv_file = request.FILES.get("file")

    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)

    count = 0
    for row in reader:
        email = row[0]
        if "@" in email:
            count = count+1
    
    data["total_email"] = count
    return JsonResponse(data)

def send_html_mails(request):
    # if request.method == "POST":
    csv_file = request.FILES.get("file")
    template_type = request.POST.get("template_type",None)
    target_user = request.POST.get("target_user",None)

    print(csv_file)
    print(template_type)
    print("--------------------------------------------------------")
    if csv_file and template_type:
        # decoded_file = csv_file.read().decode('utf-8').splitlines()
        # reader = csv.reader(decoded_file)

        # email_list = []
        # for row in reader:
        #     email = row[0]
        #     if "@" in email:
        #         email_list.append(email)

        # print(email_list)

        template_name = template_type.replace(".html","")
        x = SendBulkMail(
            target_user = target_user,
            template_name = template_name,
            location = csv_file
        )
        x.save()

        # if len(email_list)>1:
        #     send_bulk_email_comm(email_list,x.id,template_type)            
    return redirect("send_mails")

def download_report(request,id):
    print(id)
    if id:
        sendBulk_obj = SendBulkMail.objects.filter(id=id).first()
        json_result = sendBulk_obj.json_result
        print(json_result)
        print(type(json_result))

        json_result = json_result.split(",")
        print(json_result)

        response = HttpResponse(content_type = 'text/csv')
        writer = csv.writer(response)
        writer.writerow(['Email','Status'])


        for i in json_result:
            i = i.strip()
            i_split = i.split(":")
            email = i_split[0]
            result = i_split[1]
            email = email.replace("[","")
            email = email.replace("]","")
            email = email.replace("{","")
            email = email.replace("}","")
            email = email.replace("'","")

            result = result.replace("[","")
            result = result.replace("]","")
            result = result.replace("{","")
            result = result.replace("}","")
            result = result.replace("'","")
            print(email,"--",result)

            row = (
                email,
                result
            )
            writer.writerow(row)
        response['Content-Disposition'] = 'attachment; filename=BulkEmailReport-{date}.csv'.format(date=datetime.now().strftime('%d-%m-%Y'),)
        return response
    return redirect("send_mails")

def view_template(request,name):
    html_name = "email_templates/"+str(name)+".html"
    return render(request,html_name)


# def test_email(request):
    # return render(request,'email_templates/onlinetraning.html')