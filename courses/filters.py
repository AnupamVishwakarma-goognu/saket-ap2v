import django_filters
from .models import (
    Courses
)
from django.db.models import Q
import json

class CoursesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name",lookup_expr="icontains")
    fee_start = django_filters.NumberFilter(field_name='price',lookup_expr=('gte'),) 
    fee_end = django_filters.NumberFilter(field_name='price',lookup_expr=('lte'))
    duration_start = django_filters.NumberFilter(field_name='duration',lookup_expr=('gte'),) 
    duration_end = django_filters.NumberFilter(field_name='duration',lookup_expr=('lte'))

    class Meta:
        model = Courses
        fields = ['name','fee_start','fee_end','duration_start','duration_end']
