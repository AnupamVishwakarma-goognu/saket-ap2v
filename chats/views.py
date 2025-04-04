from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

# from batches.models import Batches
from batches.models import Batches
from .models import ChatFile
from django.conf import settings
from django_chatter.models import Message,Room
from users.models import CustomUserModel as User
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
from django_chatter.models import Message
import hashlib
from urllib.parse import urlparse
import urllib.request
from django_chatter.models import Room

# Create your views here.

from django_chatter.utils import create_room
from users.models import CustomUserModel as User

def create_chat_room(request,email_addresses):
    #email_addresses = ["admin@ap2v.com", "john@ap2v.com", "user@ap2v.com"]
    members = []
    # request.session['un_registered_email'] = []
    un_registered_email = []
    for email in email_addresses:
        uobj = User.objects.filter(email=email).first()
        if uobj:
            members.append(uobj)
        else:
            un_registered_email.append(email)

    room_id = create_room(members)
    # if un_registered_email:
        # request.session['un_registered_email']=un_registered_email
    return room_id

@csrf_exempt
def create_room_api(request,room_emails):
    data = {}
    for i in room_emails:
        user_obj = User.objects.filter(email = i).first()
        if not user_obj:
            x = User(
                first_name = "--",
                email = i.lower(),
                username = i,
                user_type = 'student',
            )
            x.save()
    if room_emails:
        room_id = create_chat_room(request,room_emails)
        # print(room_id)
        data['room_id'] =room_id
        # data['url'] = reverse('django_chatter:chatroom', kwargs={'uuid': room_id})
        #return redirect(reverse('django_chatter:chatroom', kwargs={'uuid': room_id}))

    return data


def chat_file_send(request):
    data={}
    if request.method == "POST":
        # file = request.FILES.get("file3")
        cont = request.POST.get("cont",1)   #count for multiple file send to name with file1, file2, file3.......file<n> 
        uuid = request.POST.get("uuid",None)
        emails = request.POST.get("emails",None)
        emails = emails.split(",")
        email_list = [x.strip(' ') for x in emails]

        for i in range(0,int(cont)):
            file = request.FILES.get("file"+str(i))
            if file:
                batch_obj = Batches.objects.filter(chat_room_id=uuid).first()
                upload_file_path = 'media/chat_files/'+str(batch_obj.id)
    
                # Check whether the specified
                # path exists or not
                print("--------------------Checking for path folder is exists or not-------------------------------------------------")
                isExist = os.path.exists(upload_file_path)
                print(isExist)
                if not isExist:
                    os.makedirs(upload_file_path)

                fs = FileSystemStorage(location=upload_file_path)
                # import uuid
                # a=uuid.uuid4()
                # a=str(a)
                print("FILE NAME : ", file.name)
                ufn=file.name
                file_format = file.name.split(".")
                file_format = file_format[-1]
                # complete_name = "AP2V_"+str(datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S'))+str('.')+str(file_format)
                if file_format == "html":
                    file_format = "htmltxt"
                complete_name = hashlib.md5(file.name.encode('utf-8')).hexdigest()+str('.')+str(file_format)
                print(complete_name)
                file = fs.save(complete_name, file)
                print("-----------------------------------------------------------------------------------------------")
                print(file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                print(fileurl)
                # fileurl = fileurl.replace("%"," ")
                fileurl= fileurl.lstrip("/")
                fileurl= fileurl.replace("media","")
                fileurl = upload_file_path+fileurl
                batch_obj = Batches.objects.filter(chat_room_id=uuid).first()

                x = ChatFile(file=file)
                if batch_obj:
                    x.batch = batch_obj.id
                x.save()

                # uuid_obj =  create_chat_room(request,final_member_list)

                y = Message(
                    sender_id = request.user.id,
                    room = Room.objects.get(id=uuid),
                    text = 'media/chat_files/'+ufn,
                    file_id = x.id
                )
                y.save()

        return JsonResponse(data)


def chat_message_send(request):
    data={}
    if request.method == "POST":
        message = request.POST.get("message",None)
        uuid = request.POST.get("uuid",None)
        emails = request.POST.get("emails",None)
        emails = emails.split(",")
        email_list = [x.strip(' ') for x in emails]

        if message:
            y = Message(
                sender_id = request.user.id,
                room = Room.objects.get(id=uuid),
                text = message,
            )
            y.save()

        return JsonResponse(data)
@login_required(login_url = '/')
def downlaod_file(request,id):
    chat_files_obj = ChatFile.objects.filter(id=id).first()
    if chat_files_obj:
        batch_id = chat_files_obj.current_batch_id_forward
        if not batch_id:
            batch_id = chat_files_obj.batch
        batch_obj = Batches.objects.filter(id=int(batch_id)).first()
        chat_room = batch_obj.chat_room_id
        room_obj = Room.objects.filter(id=chat_room).first()

        message_obj = Message.objects.filter(file_id = id).last()
        if message_obj:
            file_n = message_obj.text
            file_n = file_n.replace("media/chat_files/","")

        user_list = []
        for i in room_obj.members.all():
            user_list.append(i.email)
        # print(user_list)
        if not request.user.email in user_list:
            from django.shortcuts import render_to_response
            response = render_to_response('v4_home/error_4xx.html')
            response.status_code = 404
            return response
        else:
            file_url = '/media/chat_files/'+str(chat_files_obj.batch)+str('/')+str(chat_files_obj.file)
            print(file_url)

            if file_url.startswith('/media/'):
                file_url = settings.BASE_URL+"{}".format(file_url)
            
            filename = urlparse(file_url)
            filename = os.path.basename(filename.path)

            file_ext = filename.split(".")
            file_ext = file_ext[-1]
            if file_ext =="htmltxt":
                file_ext='html'

            try:
                response = urllib.request.urlopen(file_url)
            except Exception as e:
                print(e)
                from django.shortcuts import render_to_response
                response = render_to_response('v4_home/error_5xx.html')
                response.status_code = 403
                return response
                    
            doc_data = response.read()
            fileinfo = response.info()
            filetype = fileinfo.get('Content-Type')

            downlaodable_file_name = "AP2V Academy "+str(datetime.datetime.now().strftime('%d-%m-%Y %H.%M.%S'))+str('.')+str(file_ext)
            if message_obj:
                downlaodable_file_name = file_n

            response = HttpResponse(doc_data, content_type=filetype)
            response['Content-Disposition'] = 'inline;filename={}'.format(downlaodable_file_name)
            return response
    # return HttpResponse("Some things wents wrong.",status=404)
    from django.shortcuts import render_to_response
    response = render_to_response('v4_home/error_4xx.html')
    response.status_code = 404
    return response

@csrf_exempt
def load_all_active_chat_message_forword(request):
    context={}
    message_id = request.POST.get("message_id",None)
    batch_obj = request.POST.get("batch_obj",None)
    # print("Batch objects id: ",batch_obj)
    # print(message_id)

    context['batch_id']=batch_obj
    if message_id:
        context['message_id'] = message_id
        if request.user.user_type == "student":
            batch_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email).exclude(id=int(batch_obj))
        elif request.user.user_type == "instructor":
            batch_data = Batches.objects.filter(instructors__email = request.user.email).exclude(id=int(batch_obj))
        
        # print("--------------------------------------------------------------------------------------------------------------------------------")
        # print(batch_data)
        chat_room_list = []
        for i in batch_data:
            chat_room_list.append(i.chat_room_id)
            # print(i.chat_room_id)
            # print(i.id)
        
        # print(chat_room_list)
        # 
        rooms_list = Room.objects.filter(id__in=chat_room_list).order_by('-date_modified')[:10]
        
        context['rooms_list'] = rooms_list
        
        print(rooms_list[0].__dict__)
    return render(request,'django_chatter/forword_messagr_chat_panal.html',context)


@csrf_exempt
def chat_message_forword(request):
    import ast
    data={}
    print("-----------")

    message_id = request.POST.get("message_id",None)
    checked_batch = request.POST.get("checked_batch",None)

    checked_batch = ast.literal_eval(checked_batch)

    checked_batch_list = [int(i) for i in checked_batch]

    print(message_id)
    print(checked_batch)
    print(type(checked_batch))

    print(checked_batch_list)
    print(type(checked_batch_list))

    chat_files = Message.objects.filter(id = message_id).first()
    chat_file_id = chat_files.file_id
    print(chat_file_id)
    file_text = chat_files.text
    print(file_text)

    caht_file_obj = ChatFile.objects.filter(id=chat_file_id).first()
    file_name = caht_file_obj.file
    original_file_batch_name = caht_file_obj.batch
    print(file_name)

    
    for i in checked_batch:
        batch_obj = Batches.objects.filter(id = i).first()
        uuid = batch_obj.chat_room_id

        print("Batch id is: ",i)
        x = ChatFile(file=file_name)
        if batch_obj:
            x.batch = original_file_batch_name
            x.current_batch_id_forward = i
        x.save()

        print("Chatfile is save id is: ",x.id)

        y = Message(
            sender_id = request.user.id,
            room = Room.objects.get(id=uuid),
            text = file_text,
            file_id = x.id
        )
        y.save()

        print("Message is saved: ",y.id)

        print("------------------ Forword Complete -------------------")
    return JsonResponse(data)
