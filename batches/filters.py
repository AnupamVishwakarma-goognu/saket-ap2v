import django_filters
from .models import (
    Batches
)
from django.db.models import Q
import json

class BatchesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="batch_name",lookup_expr="icontains")
    course = django_filters.CharFilter(method="course_filter")
    user = django_filters.CharFilter(method="user_filter")
    start_date_start = django_filters.DateFilter(field_name='start_date_time',lookup_expr=('gte'),) 
    start_date_end = django_filters.DateFilter(field_name='start_date_time',lookup_expr=('lte'))

    duration_start = django_filters.NumberFilter(field_name='duration',lookup_expr=('gte'),) 
    duration_end = django_filters.NumberFilter(field_name='duration',lookup_expr=('lte'))

    created_on_start = django_filters.DateFilter(field_name='added_on',lookup_expr=('gte'),) 
    created_on_end = django_filters.DateFilter(field_name='added_on',lookup_expr=('lte'))

    class Meta:
        model = Batches
        fields = ['name','course','user','start_date_start','start_date_end','duration_start','duration_end','created_on_start','created_on_end']


    def course_filter(self,q,n,v):
        return q.filter(courses__in=v.split(','))
    

    def user_filter(self,q,n,v):
        return q.filter(instructors_id__in=v.split(','))
