import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anquira_v2.settings")
django.setup()

from enquiries.models import *

"""
course_obj = Courses.objects.get(id=210)

#enq = Enquiries.objects.get(id=51)
#EnquiryCourses.objects.get(enquiry_id=enq)
#EnquiryCourses.objects.create(enquiry_id=enq, courses=course_obj)

for e in Enquiries.objects.all():
    aws_course_count = EnquiryCourses.objects.filter(enquiry_id=e, courses=course_obj).count()
    aws_course = EnquiryCourses.objects.filter(enquiry_id=e, courses=course_obj).order_by("id").last()

    if aws_course_count > 1:
        print(aws_course_count, e.id)
        print(aws_course.delete())
    #EnquiryCourses.objects.create(enquiry_id=e, courses=course_obj)
"""

for e in Enquiries.objects.all():
    discard_count = EnquiryCourses.objects.filter(enquiry_id=e, discard=True).count()
    total_count = EnquiryCourses.objects.filter(enquiry_id=e).count()

    if discard_count == total_count and e.discard == False:
        print(e.id)

