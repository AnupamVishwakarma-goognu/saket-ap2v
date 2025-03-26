from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta,datetime
from communication.views import send_batch_join_alert_email
from ap2v_courses.models import Courses,Lessons,Course_FQA,Industry_Projects,City_Specific_Course,CitySpecificCoursesFQA

from testimonials.models import Text
import csv
from django.http import HttpResponse, JsonResponse
import os



class Command(BaseCommand):
    help = 'Validate the courses details, if course id=s complete or not.'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        course_obj = Courses.objects.all()

        # f = open('D:/file.csv', 'w')
        f = open('/tmp/file.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['Type','id','url','Missing-Fields'])

        for i in course_obj:
            print("Checking for course id : ",i.id)

            list = []
            
            #checking for course content................
            lesson_obj = Lessons.objects.filter(course=i.id)
            if not lesson_obj:
                list.append(" Lession")
            
            #checking Review:
            review_obj = Text.objects.filter(course=i.id)
            if not review_obj:
                list.append(" Review")
            
            #checking FAQ:
            faq_obj = Course_FQA.objects.filter(belong_course=i.id)
            if not faq_obj:
                list.append(" FAQ")
            
            #checking Project:
            project_obj = Industry_Projects.objects.filter(belong_course=i.id)
            if not project_obj:
                list.append(" Project")

            related_course = i.category_name.all()
            if not related_course:
                list.append("Related Category Course")


            # response = HttpResponse(content_type = 'text/csv')
            
            if len(list) >0:
                row = (
                    'Parent',
                    i.id,
                    i.slug,
                    list
                )
                writer.writerow(row)



        city_specific_course = City_Specific_Course.objects.all()
        for j in city_specific_course:
            print("Checking for City Specific course id : ",i.id)
            city_specific_faq = CitySpecificCoursesFQA.objects.filter(belong_city_spqcific_course = j.id)
            if not city_specific_faq:
                row = (
                    'Child',
                    j.id,
                    j.slugs,
                    "City FAQ"
                )
                writer.writerow(row)
        # response['Content-Disposition'] = 'attachment; filename=BulkEmailReport'
        f.close()
        # return response





