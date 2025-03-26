import django_filters
from enquiries.models import (
    Followups
)
from django.db.models import Q
import json
import datetime as dt
from datetime import timedelta
from anquira_v2.anquira_handlers import ReferenceModeChoices


class FollowupFilter(django_filters.FilterSet):
    d = django_filters.CharFilter(method="dayfilter")
    name = django_filters.CharFilter(method="name_filter")
    mobile = django_filters.CharFilter(method="mobile_filter")
    email = django_filters.CharFilter(method="email_filter")
    reference = django_filters.CharFilter(method="reference_filter")
    course = django_filters.CharFilter(method="course_filter")
    location = django_filters.CharFilter(method="location_filter")
    owner = django_filters.CharFilter(method="owner_filter")
    start_date = django_filters.DateFilter(field_name='next_followup',lookup_expr=('gte'),) 
    end_date = django_filters.DateFilter(field_name='next_followup',lookup_expr=('lte'))
    is_completed = django_filters.BooleanFilter(method="is_completed_filter")
    discarded = django_filters.BooleanFilter(method="discarded_filter")

    class Meta:
        model = Followups
        fields = ['id','d','name','mobile','email','reference','course','location','owner','start_date','end_date', 'is_completed', 'discarded']

    def is_completed_filter(self, queryset, name, value):
        print(v)
        return q.filter(is_complete=v)

    def discarded_filter(self, queryset, name, value):
        return q.filter(followupid__discard=v)

    def owner_filter(self,q,n,v):
        return q.filter(assigned_user_id=v)

    def location_filter(self,q,n,v):
        return q.filter(followupid__branch_location=v)

    def reference_filter(self,q,n,v):
        return q.filter(followupid__reference__in=v.split(','))

    def course_filter(self,q,n,v):
        return q.filter(followupid__enquirycourses__courses_id__in=v.split(','))
    
    def name_filter(self, queryset, name, value):
        return  queryset.filter(followupid__full_name__icontains=value)
   
    def mobile_filter(self, queryset, name, value):
        return  queryset.filter(Q(followupid__mobile__icontains=value)|Q(followupid__alternative_mobile__icontains=value))

    def email_filter(self, queryset, name, value):
        return  queryset.filter(Q(followupid__email__icontains=value)|Q(followupid__alternative_email__icontains=value))

    def dayfilter(self, queryset, name, value):
        if value == 'pending':
            queryset_var = queryset.filter(
                next_followup__gte=dt.date.today(),
                next_followup__lte=dt.date.today() + timedelta(1),
                # followupid__discard=False,
                #is_complete=False
            )#.order_by('-next_followup')
        elif value == 'overdue':
            queryset_var = queryset.filter(
                next_followup__lte=dt.date.today(),
                # followupid__discard=False,
                #is_complete=False
            )#.order_by('-next_followup')
        elif value == 'tomorrow':
            queryset_var = queryset.filter(
                next_followup__gte=dt.date.today() + timedelta(1),
                next_followup__lte=dt.date.today() + timedelta(2),
                # followupid__discard=False,
                #is_complete=False
            )#.order_by('-next_followup')
        else:
            queryset_var = queryset.filter(
                next_followup__gte=dt.date.today(),
                next_followup__lte=dt.date.today() + timedelta(1),
                # followupid__discard=False,
                #is_complete=False
            )#.order_by('-next_followup')
        return queryset_var

class FollowupsNameFilter(django_filters.FilterSet):
    n = django_filters.CharFilter(method="n_filter_method")

    class Meta:
        model = Followups
        fields = ['n']

    def n_filter_method(self, queryset, name, value):
        queryset_var = queryset
        type_value, name_value = json.loads(value.replace("'",'"')).get('type'), json.loads(value.replace("'",'"')).get('n')
        if type_value == "name":
            queryset_var = queryset.filter(
                full_name__icontains=name_value
            )
        elif type_value == 'email':
            queryset_var = queryset.filter(
                Q(email__icontains=name_value) | Q(alternative_email__icontains=name_value)
            )
        elif type_value == 'number':
            queryset_var = queryset.filter(
                Q(mobile__icontains=name_value | Q(alternative_mobile__icontains=name_value))
            )
        return queryset_var.order_by('-id')
