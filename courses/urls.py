from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('add/', views.courses, name="courses"),
    path('list/', views.courseslist, name="courseslist"),
    re_path(r'view/(?P<courses_id>[\w]+)/$', views.courseView, name='courseView'),
    re_path(r'update_coures/(?P<course_id>[\d]+)/$', views.UpdateCourseView.as_view(), name="update_coures"),
    re_path(r'(?P<pk>\d+)/delete/$', views.CoursesDeleteView.as_view(), name="CoursesDeleteView"),
    path('add/exam', views.exams, name="exams"),
    path('list/exam', views.examslist, name="examslist"),

    path('books/', views.books, name="books"),
    path('add_book/', views.add_book, name="add_book"),
    path('add_book_stock/', views.add_book_stock, name="add_book_stock"),
]
