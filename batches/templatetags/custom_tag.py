from django import template
from urllib.parse import urlencode
from courses.models import Courses
from enquiries.models import EnquiryCourses

register = template.Library()

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter(name="days_of_week_instructor_short")
def days_of_week_short(value):
    return ", ".join([i[:3] for i in value.split(',')])


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()

@register.filter(name='convt')
def convt(key,value):
    print(key)
    # print(value)
    return str(key)

@register.filter(name='sp_name')
def sp_name(key,value):
    print(key)
    # print(value)
    key = key.split(',')
    # print(key)
    course_lis = []
    for i in key:
        print(i)
        a = Courses.objects.filter(id = int(i)).first()
        if a:
            course_lis.append(a.name)
        else:
            a = EnquiryCourses.objects.filter(id=int(i)).first()
            if a:
                course_lis.append(a.courses.name)
    return course_lis

@register.filter
def get_skill(skills):
    print(skills)
    try:
        skill_point = skills.split(",")
    except:
        skill_point = ['N/A','N/A']
    # skill_point = ['DevOps methodologies', 'Version control systems', 'Jenkins TeamCity Maven', 'Continuous integration and deployment']
    return skill_point