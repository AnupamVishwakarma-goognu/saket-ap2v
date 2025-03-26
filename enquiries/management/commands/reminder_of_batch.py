import json
from django.core.management.base import BaseCommand, CommandError
from classroom.views import weeknum
from batches.models import Batches,BatchSessionOff,PublicHoliday
from datetime import timedelta
from django.utils import timezone
import pytz
import datetime
from datetime import datetime, date

from communication.views import send_batch_reminder


class Command(BaseCommand):
    help = 'This Script Remind the instructor before veriable time.'

    def handle(self, *args, **kwargs):
        tz_NY = pytz.timezone('Asia/Kolkata')   
        # now = datetime.now() + timedelta(hours=5,minutes=30)
        now = datetime.now(tz_NY)

        all_batch_obj = Batches.objects.filter(complete=False)
        all_batch_obj = all_batch_obj.filter(end_date_time__gte = now)

        today_date = []
        public_holiday_obj = PublicHoliday.objects.filter(off_date = datetime.now().date())
        if not public_holiday_obj:
            for i in all_batch_obj:
                batch_start_date = i.start_date_time.date()
                batch_end_date = i.end_date_time.date()

                start_time = (i.start_date_time + timedelta(hours=5,minutes=30)).time()

                course_list = []
                for j in i.courses.all():
                    course_list.append(j.name)

                days = i.days_of_week.split(",")
                for day in days:
                    whichDayYouWant = day
                    days_date = [batch_start_date + timedelta(days=x) for x in range((batch_end_date-batch_start_date).days + 1) if (batch_start_date + timedelta(days=x)).weekday() == weeknum(whichDayYouWant)]
                    for d in days_date:
                        if d == date.today():
                                # start = datetime.combine(d,start_time) + timedelta(hours=5,minutes=30)
                                start = datetime.combine(d,start_time)
                                now_inc = now
                                now_inc = now_inc.strftime("%H:%M:%S")

                                print("Batch id : ", i.id,"  ",end="")
                                print("Batch Start Time : ",start_time,"  ",end="")
                                print("Now Time : ", now_inc,"  ",end="")

                                import datetime as dt
                                now_inc = (dt.datetime.strptime(now_inc, '%H:%M:%S').time())
                                a1 = start_time
                                b1 = now_inc
                                duration = datetime.combine(now.date(), a1) - datetime.combine(now.date(), b1)
                                print("Time Difference : ",duration.total_seconds() / 60,"  ",end="")
                                difference = duration.total_seconds() / 60

                                if difference>=45 and difference<=59:
                                    # print("Sending Mail","  ",end="")

                                    batch_off_session = BatchSessionOff.objects.filter(batch=i.id, off_date = d)
                                    if not batch_off_session:                                
                                        reminder_log = i.reminder_log

                                        today_date = date.today()
                                        if reminder_log:
                                            json_acceptable_string = reminder_log.replace("'", "\"")
                                            reminder_log = json.loads(json_acceptable_string)
                                        
                                        today_date2 = str(date.today())
                                        if reminder_log:
                                            if today_date2 in reminder_log:
                                                print("Do Nothings... Alert already sent.")
                                            else:
                                                print("Sending Mail","  ",end="")
                                                reminder_log[today_date2] = "Email Sent"
                                                Batches.objects.filter(id=i.id).update(
                                                    reminder_log = reminder_log
                                                )
                                                send_batch_reminder(i.id)
                                        else:
                                            print("Sending Mail","  ",end="")
                                            reminder_log = {}
                                            reminder_log[today_date2] = "Email Sent"
                                            Batches.objects.filter(id=i.id).update(
                                                reminder_log = reminder_log
                                            )
                                            send_batch_reminder(i.id)
                                    else:
                                        print("Today is off for this batch.")
                                else:
                                    print("Batch time not in under 59M.Not Sending Alert.")
        else:
            print("Today is public holiday so not sending any email.")
            

