from django.core.management.base import BaseCommand
# from django.utils import timezone
import datetime
import pytz
from django.utils import timezone as tz
from enquiries.models import Enquiries,ReassignedEnquiryLogs
from users.models import CustomUserModel as User
from users.models import CounselorPreferences
import random
from django.conf import settings
from communication.views import send_enquiry_resign_mail


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        utc=pytz.UTC

        start_hours = 10
        end_hours = 20

        #time in minutes
        reshuffle_hour = 15
        # reshuffle_hour = 1
        counselor_list = settings.COUNSELOR_LIST


        # if datetime() > 9am and < 6pm then consider 9am
        office_hours_start = utc.localize(datetime.datetime.now().replace(hour=start_hours, minute=15)) #(Morning 9 AM)
        office_hours_end = utc.localize(datetime.datetime.now().replace(hour=end_hours, minute=0))
        # office_hours_end_previous_day = utc.localize(datetime.datetime.now().replace(hour=end_hours, minute=0) - datetime.timedelta(days=1))# (Evening 6 PM)

        
        print(office_hours_start)
        print(office_hours_end)

        current_date_time = datetime.datetime.now()
        # current_date_time = datetime.datetime(2021, 9, 30, 20, 55, 59, 342380)
        print(current_date_time)

        if current_date_time.time() >=office_hours_start.time() and current_date_time.time() <= office_hours_end.time():

            # geting all enquires from last 2 day's
            d = tz.now() - datetime.timedelta(days=2)
            enq_obj = Enquiries.objects.filter(added_on__gte=d,junk=False)
            enq_obj = enq_obj.filter(attended = False)
            print("Unattended Enq : ",enq_obj)

            after_hour = tz.now()-tz.timedelta(minutes=reshuffle_hour)
            print("After Hour: ",after_hour)
            enq_obj = enq_obj.filter(assigned_on__lte = after_hour)

            print("15 Min Enq obj: ",enq_obj)

            for i in enq_obj:
                print("Enguiry id is: ",i.id)
                ad=i.assigned_on
                # at=i.attended.assigned_on
                print('This assigned on time: ',ad) 
                print("Added on: ",i.added_on) 
                print('This now:',datetime.datetime.now())
                print("TZ Now : ",tz.now())
                print("*"*30)

                
                # geting all counselor except one(already assigned)
                # user_obj = User.objects.filter(user_type = "counselor").exclude(id=i.assigned_by_id)

                # choose random one into all of them except one(already assigned)
                # random_item = random.choice(user_obj)   
                
                # enq_assigned_id = Enquiries.objects.filter(id=i.id).first().assigned_by_id
                # # print("enq_assigned_id:",enq_assigned_id)
                # index_of_counselor = counselor_list.index(enq_assigned_id)
                # # print("index_of_counselor:",index_of_counselor)
                # index_of_counselor=index_of_counselor+1
                
                # if len(counselor_list) == index_of_counselor:
                #     index_of_counselor = counselor_list.index(enq_assigned_id)
                #     index_of_counselor = index_of_counselor-1

                # # print(index_of_counselor)

                # # print(counselor_list[index_of_counselor])
                # u_id = counselor_list[index_of_counselor]

                

                get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                print(get_counselor)
                # print(get_counselor.user)
                if get_counselor is None:
                    all_counselor = CounselorPreferences.objects.all()
                    for i in all_counselor:
                        CounselorPreferences.objects.filter(id=i.id).update(
                        last_assigned=False
                        )
                    get_counselor = CounselorPreferences.objects.filter(last_assigned = False).first()
                print(get_counselor)
                print(get_counselor.user)

                Enquiries.objects.filter(id=i.id).update(
                    assigned_by = get_counselor.user.id,
                    assigned_on = tz.now()
                )

                x = ReassignedEnquiryLogs(
                    enquiry_id = i.id,
                    from_counselor_id = i.assigned_by_id,
                    to_counselor_id = get_counselor.user.id
                )
                x.save()

                CounselorPreferences.objects.filter(id=get_counselor.id).update(
                    last_assigned=True
                )

                old_counselor = User.objects.filter(id=i.assigned_by_id).first().first_name
                new_counselor = User.objects.filter(id=get_counselor.user.id).first().first_name
                print("Sending mail.....")
                send_enquiry_resign_mail(i.id, old_counselor, new_counselor)
                
        # from django.core.mail import send_mail
        # send_mail(
        # 'testing purpose',
        # 'this is my testing purpose.',
        # 'aashish@goognu.com',
        # ['aashishchhachhiya@gmail.com'],
        # fail_silently=False,
        # )
