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

"""
for e in Enquiries.objects.all():
    discard_count = EnquiryCourses.objects.filter(enquiry_id=e, discard=True).count()
    total_count = EnquiryCourses.objects.filter(enquiry_id=e).count()

    if discard_count == total_count and e.discard == False:
        print(e.id)
"""

for e in Enquiries.objects.all():
#for e in Enquiries.objects.filter(id=8053):
    #non_uniq = EnquiryCourses.objects.filter(enquiry_id=e).values('courses_id').count()
    #uniq = EnquiryCourses.objects.filter(enquiry_id=e).values('courses_id').distinct().count()
    #if non_uniq != uniq:
    if True:
        #print(e.id)
        #exit()
        uniq_ids = []
        for row in EnquiryCourses.objects.filter(enquiry_id=e):
            if row.courses_id not in uniq_ids:
                uniq_ids.append(row.courses_id)
            else:
                print("Deleting: ",row.id)
                #row.delete()
                print(e.id)
        #print(uniq_ids)

        #exit()
