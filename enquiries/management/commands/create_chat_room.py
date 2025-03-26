from django.core.management.base import BaseCommand
import datetime
import random
from chats.views import create_room_api
from batches.models import Batches

class Command(BaseCommand):
    help = 'Create Chat Rooms for Batches which is not created.'
    def handle(self, *args, **kwargs):
        batch_obj = Batches.objects.all()
        print(batch_obj)
        print("Total Batch Found : ",batch_obj.count())

        for i in batch_obj:
            print("Process Start for Batch id : ",i.id)
            room_email = []
            all_student = i.enroll_student.all()
            for j in all_student:
                # print(j.enquiry_course_id.enquiry_id.email,end=", ")
                room_email.append(j.enquiry_course_id.enquiry_id.email)
            room_email.append(i.instructors.email)
            print(room_email)
            print("Total emails enroll in batch with instructore : ", len(room_email))

        
            data = create_room_api(self,room_email)
            print("Room id Created : ",data['room_id'])
            print("Student and Instructor added in room.")
            if data['room_id']:
                Batches.objects.filter(id=i.id).update(
                chat_room_id = data['room_id'])

            print("Process Complete for Batch")
            print("-------------------------------------------------------------------------------------------------------------------------------------")