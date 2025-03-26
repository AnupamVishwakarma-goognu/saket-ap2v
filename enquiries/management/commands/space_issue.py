from django.core.management.base import BaseCommand
from ap2v_courses.models import Courses


class Command(BaseCommand):
    help = 'Correct Space Issue in content and other text data'
    def handle(self, *args, **kwargs):
        course_obj = Courses.objects.all()

        for i in course_obj:
            banner_text = i.banner_text
            # print(banner_text)
            # print("-------------------------------")
            banner_text = banner_text.replace("<b>"," <b> ")
            banner_text = banner_text.replace("</b>"," </b> ")
            # print(banner_text)

            x = Courses.objects.filter(id = i.id).first()

            x.banner_text = banner_text

            x.save()