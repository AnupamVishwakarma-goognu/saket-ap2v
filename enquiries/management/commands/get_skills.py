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

        # f = open('D:/course_skills-tags.csv', 'w')
        f = open('/tmp/course_skills-tags.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['Id','course Name','URL','Skills/Tags'])

        for i in course_obj:
            skill_list = []
            skills = i.tags.all()
            # print(skills)

            for j in skills:
                # print(j)
                skill_list.append(str(j))
            if len(skill_list) >0:
                row = (
                    i.id,
                    i.name,
                    i.slug,
                    skill_list
                )
                writer.writerow(row)