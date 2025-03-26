import django_filters
from .models import (
    Instructors
)
from django.db.models import Q
import json

class InstructorsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="full_name",lookup_expr="icontains")
    course = django_filters.CharFilter(method="course_filter")
    weekday = django_filters.CharFilter(method="weekday_filter")
    
    class Meta:
        model = Instructors
        fields = ['name','course','weekday']


    def course_filter(self,q,n,v):
        return q.filter(courses__in=v.split(','))
    
    def weekday_filter(self,q,n,v):
        
        query = None
        for wk in v.split(','):
            if query is None:
               query = Q(days_of_week__icontains=wk)
            else:
                query |= Q(days_of_week__icontains=wk)
        return q.filter(query)