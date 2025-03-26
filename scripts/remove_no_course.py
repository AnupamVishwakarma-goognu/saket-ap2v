import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anquira_v2.settings")
django.setup()

from enquiries.models import *
from courses.models import *

ec = Courses.objects.get(id=139)

for e in Enquiries.objects.all():
    total_courses = EnquiryCourses.objects.filter(enquiry_id=e).count()
    no_course_count = EnquiryCourses.objects.filter(enquiry_id=e,courses=ec).count()

    if no_course_count > 0 and total_courses != no_course_count:
        print(e.id)
        EnquiryCourses.objects.filter(enquiry_id=e,courses=ec).delete()
        #exit()

    """
    e_obj = Enquiries.objects.get(id=int(e))
    try:
        EnquiryCourses.objects.create(enquiry_id=e_obj, courses=ec)
    except:
        pass
    """
    #exit()
