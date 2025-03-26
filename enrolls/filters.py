import django_filters
from .models import (
    Enrollments,Installments
)
from courses.models import Courses
from django.db.models import Q
import json

class EnrollmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="name_filter")
    course = django_filters.CharFilter(method="course_filter")
    mobile = django_filters.CharFilter(method="mobile_filter")
    refund_amount = django_filters.CharFilter(field_name="refund_amount",lookup_expr="icontains")
    refund = django_filters.CharFilter(field_name="refund",lookup_expr="icontains")
    dropped = django_filters.CharFilter(field_name="dropped",lookup_expr="icontains")
    certificate_issued = django_filters.CharFilter(field_name="certificate_issued",lookup_expr="icontains")
    enroll_type = django_filters.CharFilter(field_name="enroll_type",lookup_expr="icontains")
    
    discussed_fee_start = django_filters.NumberFilter(field_name='discussed_fee',lookup_expr=('gte'),) 
    discussed_fee_end = django_filters.NumberFilter(field_name='discussed_fee',lookup_expr=('lte'))

    registration_amount_start = django_filters.NumberFilter(field_name='registration_amount',lookup_expr=('gte'),) 
    registration_amount_end = django_filters.NumberFilter(field_name='registration_amount',lookup_expr=('lte'))

    registered_by = django_filters.CharFilter(field_name="registered_by",lookup_expr="icontains")
    start_date = django_filters.DateFilter(field_name='registered_on',lookup_expr=('gte'),) 
    end_date = django_filters.DateFilter(field_name='registered_on',lookup_expr=('lte'))
    class Meta:
        model = Enrollments
        fields = ['name','course','mobile','discussed_fee_start','discussed_fee_end','registration_amount_start','registration_amount_end','registered_by','start_date','end_date','refund','refund_amount','dropped','certificate_issued','enroll_type']
    
    def name_filter(self,q,n,v):
        return q.filter(enquiry_course_id__enquiry_id__full_name__icontains=v)

    def mobile_filter(self,q,n,v):
        return q.filter(enquiry_course_id__enquiry_id__mobile__icontains=v)

    def course_filter(self,q,n,v):
        return q.filter(enquiry_course_id__courses__in=v.split(','))
    


class FeesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="name_filter")
    course = django_filters.CharFilter(method="course_filter")
    batch = django_filters.CharFilter(method="batch_filter")
    
    due_date_start = django_filters.DateFilter(field_name='due_date',lookup_expr=('gte'),) 
    due_date_end = django_filters.DateFilter(field_name='due_date',lookup_expr=('lte'))

    class Meta:
        model = Installments
        fields = ['name','course','batch','due_date_start','due_date_end']
    
    def name_filter(self,q,n,v):
        return q.filter(enrollmentid__enquiry_course_id__enquiry_id__full_name__icontains=v)

    def course_filter(self,q,n,v):
        return q.filter(enrollmentid__enquiry_course_id__courses__in=v.split(','))
    
    def batch_filter(self,q,n,v):
        return q.filter(enrollmentid__batch__batch_name__icontains=v)
