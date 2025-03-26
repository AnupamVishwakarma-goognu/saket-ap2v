from django.core.management.base import BaseCommand
from courses.models import Courses
from django.conf import settings
import os
import csv

class Command(BaseCommand):
    help = 'Update the anquira course price from csv'

    def handle(self, *args, **kwargs):
        # csv_path = os.path.join(settings.STATICFILES_DIRS,str('course_price.csv'))
        with open('course_price.csv','r') as f:
            r = csv.reader(f)
            number = 1
            for row in r:
                if number >2:
                    print(row)
                    print("Id:",row[0])
                    print("Name:",row[1])
                    print("Price:",row[2])
                    print("Is GST:",row[3])
                    print("Is Exam:",row[4])
                    print("Expired:",row[5])
                    if row[5] == "Expired":
                        # print("Expaired: Yes")
                        is_expired = True
                    else:
                        # print("Expaired: No")
                        is_expired = False

                    try:
                        rid = int(row[0])
                    except Exception as e:
                        print(e)
                    
                    try:
                        cprice = int(row[2])
                    except Exception as e:
                        print(e)
                    
                    if row[4].strip()=="Yes":
                        ctype = 2
                        is_exam = True
                        print("Entering in IF")
                    else:
                        ctype = 1
                        is_exam = False
                        print("Entering in ElseIF")

                    if row[3]=="Yes":
                        is_gst = True
                    else:
                        is_gst = False
                    
                    # print(rid,cprice)
                    
                    if rid:
                        course_obj_row = Courses.objects.filter(id=rid).first()
                        if course_obj_row:
                            print(rid,"Found")
                            Courses.objects.filter(id=rid).update(
                                name = row[1],
                                price = cprice,
                                typee = ctype,
                                is_exam = is_exam,
                                is_expired = is_expired,
                                is_gst = is_gst

                            )
                            print("Updated")
                        else:
                            print(rid,"Not Found")
                            x = Courses(
                                id = rid,
                                name = row[1],
                                price = cprice,
                                typee = ctype,
                                is_exam = is_exam,
                                duration = 0,
                                url = "https://www.ap2v.com/",
                                is_expired = is_expired,
                                is_gst = is_gst

                            )
                            x.save()
                            print("Created with id: ",x.id )
                    print("---------------------------")
                number=number+1