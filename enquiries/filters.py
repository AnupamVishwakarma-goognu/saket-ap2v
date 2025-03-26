import django_filters
from .models import (
    Enquiries
)
from courses.models import Courses
from django.db.models import Q
import json

class EnquiryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="full_name",lookup_expr="icontains")

    mobile = django_filters.CharFilter(method="mobile_filter")
    email = django_filters.CharFilter(method="email_filter")
    reference = django_filters.CharFilter(method="reference_filter")
    course = django_filters.CharFilter(method="course_filter")
    location = django_filters.CharFilter(method="location_filter")

    start_date = django_filters.DateFilter(field_name='added_on',lookup_expr=('gte'),) 
    end_date = django_filters.DateFilter(field_name='added_on',lookup_expr=('lte'))

    batch_preference = django_filters.CharFilter(field_name="batch_days",lookup_expr="icontains")
    interest_level = django_filters.CharFilter(field_name="enquiry_level")
    owner = django_filters.CharFilter(method="owner_filter")
    interested_batch = django_filters.BooleanFilter(field_name='interested_batch')
    # discarded = django_filters.BooleanFilter(method='discard_filter')
    company_name = django_filters.CharFilter(field_name="company_name",lookup_expr="icontains")
    designation = django_filters.CharFilter(field_name="designation",lookup_expr="icontains")
    class Meta:
        model = Enquiries
        fields = ['name','mobile','email','reference','course','location','start_date','end_date','batch_preference',\
                'training_mode','interest_level','owner','interested_batch','company_name','designation']
    
        
    def mobile_filter(self, queryset, name, value):
        return  queryset.filter(Q(mobile__icontains=value)|Q(alternative_mobile__icontains=value))

    def email_filter(self, queryset, name, value):
        return  queryset.filter(Q(email__icontains=value)|Q(alternative_email__icontains=value))

    def reference_filter(self,q,n,v):
        return q.filter(reference__in=v.split(','))

    def course_filter(self,q,n,v):
        #return q.filter(courses__in=v.split(','))
        return q.filter(enquirycourses__courses__in=v.split(','))
    
    def location_filter(self,q,n,v):
        return q.filter(branch_location__icontains=v)

    def owner_filter(self,q,n,v):
        return q.filter(followups__assigned_user_id=v)
