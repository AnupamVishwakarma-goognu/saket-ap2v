import django_filters
from django.db.models import Q
from ap2v_courses.models import Courses
from itertools import chain

class CoursesCategoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category_name__slug', lookup_expr='icontains') #, method='category_filter')
    
    class Meta:
        model = Courses
        fields = ['category']

    #def category_filter(self, queryset, name, value):
    #    return Courses.objects.all()


class SearchDataFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Courses
        fields = ['q']

    def search_filter(self, queryset, name, value):
        q_value = value.replace('-', ' ')
        courses_qs = queryset.filter(
                        Q(name__icontains=q_value) | Q(Text_Blog__icontains=q_value) | Q(description__icontains=q_value)
                    )
        return courses_qs
