from django.core.management.base import BaseCommand, CommandError
from classroom.views import weeknum
from batches.models import Batches
from datetime import timedelta
from django.utils import timezone
import pytz
import datetime
from communication.views import send_batch_join_alert_email


class Command(BaseCommand):
    help = 'Geting all batch recording data'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()

        # print("Current Time : ", now)

        all_batch_obj = Batches.objects.filter(complete=False)
        all_batch_obj = all_batch_obj.filter(end_date_time__gte = now)

        today_date = []
        for i in all_batch_obj:
            batch_start_date = i.start_date_time.date()
            batch_end_date = i.end_date_time.date()

            start_time = i.start_date_time.time()

            course_list = []
            for j in i.courses.all():
                course_list.append(j.name)

            days = i.days_of_week.split(",")
            for day in days:
                whichDayYouWant = day
                days_date = [batch_start_date + timedelta(days=x) for x in range((batch_end_date-batch_start_date).days + 1) if (batch_start_date + timedelta(days=x)).weekday() == weeknum(whichDayYouWant)]
                for d in days_date:
                    if d == datetime.date.today():
                            start = datetime.datetime.combine(d,start_time) + timedelta(hours=5,minutes=30)
                            start = start+timedelta(minutes=3)
                            # print(start.time())
                            if now.time() > start.time():
                                print("Passed")
                                if i.last_join_datetime:
                                    if not i.last_join_datetime.date == now.date():
                                        if i.is_alert_send == False:
                                            today_batch_date = {}
                                            today_batch_date['title'] = " and ".join(course_list)
                                            today_batch_date['start'] = start
                                            today_batch_date['email'] = i.instructors.email
                                            today_date.append(today_batch_date)

                                            print("Sending Email...")
                                            send_batch_join_alert_email(i.instructors.email, "and ".join(course_list))

                                            Batches.objects.filter(id=i.id).update(is_alert_send=True)
                                        else:
                                            print("Already alert send")
                                else:
                                    if i.is_alert_send == False:
                                        today_batch_date = {}
                                        today_batch_date['title'] = " and ".join(course_list)
                                        today_batch_date['start'] = start
                                        today_batch_date['email'] = i.instructors.email
                                        today_date.append(today_batch_date)

                                        print("Sending Email...")
                                        send_batch_join_alert_email(i.instructors.email, "and ".join(course_list))

                                        Batches.objects.filter(id=i.id).update(is_alert_send=True)
                                    else:
                                        print("Already alert send")
                            else:
                                print("Not passed")
                        
                        
            # print(today_date)
            # print("-----------------------------------")
            

