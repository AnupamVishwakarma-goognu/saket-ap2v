from django import template
from batches.models import Batches
register = template.Library()
import re


@register.simple_tag
def get_skill(skills):
    print(skills)
    try:
        skill_point = skills.split(",")
    except:
        skill_point = ['N/A','N/A']
    # skill_point = ['DevOps methodologies', 'Version control systems', 'Jenkins TeamCity Maven', 'Continuous integration and deployment']
    return skill_point

@register.simple_tag
def get_batch_details(batch_id):
    print("---------------------------------------")
    print(batch_id)
    if batch_id:
        print("---------------------------------------")
        print(batch_id)
        batch_obj = Batches.objects.filter(id=batch_id).first()
    return batch_obj

@register.simple_tag
def get_week_days(weeks):
    if weeks:
        wd = ','.join(x[0:3] for x in weeks.split(','))        
    return wd
