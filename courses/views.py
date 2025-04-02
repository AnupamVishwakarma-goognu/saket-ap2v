from django.shortcuts import render, redirect
from .models import Courses, Exams,Books
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .filters import (
    CoursesFilter
)
from django.core.paginator import Paginator
from anquira_v2.decorators import custome_check

@login_required(login_url = '/')
@custome_check()
def courses(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            duration = request.POST.get('duration', '').strip()
            url = request.POST.get('url', '').strip()
            price = request.POST.get('price', '').strip()
            course_content = request.FILES.get('course_content')
            is_exam = request.POST.get("is_exam", False)
            # course_type = request.POST.get("course_type", None)

            if not name or not duration or not url or not price:
                return JsonResponse({"success": False, "message": "All fields are required!"}, status=400)
            Courses.objects.create(
                name=name, 
                duration=duration, 
                url=url, 
                price=price, 
                course_content=course_content, 
                is_exam=is_exam, 
                # typee=course_type
            )

            return JsonResponse({"success": True, "message": "Course added successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return render(request, 'courses/course_form.html', {})


@login_required(login_url="/")
@custome_check()
def courseslist(request):
    ctx = {}
    is_exam = request.GET.get("exam",None)
    print(is_exam)
    if is_exam:
        courses = Courses.objects.filter(is_exam=True).order_by('name')
        ctx['exam'] = 'true'
    else:
        courses = Courses.objects.filter(is_exam=False).order_by('name')
    
    data = request.GET.copy()
    courses = CoursesFilter(data, courses).qs

    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    try:
        courses = paginator.page(page_number)
    except:
        courses = paginator.page(1)
    
    ctx['courses']=courses
    return render(request, 'courses/list.html', ctx)

@login_required(login_url="/")
@custome_check()
def courseView(request, courses_id):
    courses = Courses.objects.get(id=courses_id)
    return render(request, 'courses/course_view.html', {'courses':courses})

class UpdateCourseView(View):
    redirect_url = "courseslist"

    def post(self, *args, **kwargs):
        course_obj = Courses.objects.filter(
            id=self.kwargs.get('course_id')
        )
        if course_obj.exists():
            course_obj.update(
                name=self.request.POST.get('name'),
                duration=self.request.POST.get('duration'),
                price=self.request.POST.get('price'),
                url=self.request.POST.get('url'),
                is_exam = self.request.POST.get("is_exam",False)

            )
            if self.request.FILES.get('course_content'):
                course_obj_new = course_obj.get()
                course_obj_new.course_content = self.request.FILES['course_content']
                course_obj_new.save()
        response_data = {
            'status': 1,
            'redirect': reverse(self.redirect_url)
        }
        return JsonResponse(response_data)

class CoursesDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/'
    model = Courses
    success_url = reverse_lazy('courseslist')

    def get(self, *args, **kwargs):
        r_dict = {
            'status': None,
        }
        try:
            self.delete(self.request, *args, **kwargs)
            r_dict.update(status=1)
            return JsonResponse(r_dict)
        except:
            r_dict.update(status=0)
            return JsonResponse(r_dict)

@login_required(login_url = '/')
@custome_check()
def exams(request):
    context_data={}
    if request.method == 'POST':
        exam_name = request.POST['exam_name']
        # print(exam_name)
        courses_id_list = ",".join(request.POST.getlist('course'))
        courses_id_list = courses_id_list.split(",")
        # print(courses_id_list)

        for i in courses_id_list:
            x = Exams(
                exam_name = exam_name, 
                courses=Courses.objects.get(id = int(i))
            )
            x.save()
    else:
        context_data['course'] = Courses.objects.all().order_by('name')

    return render(request, 'courses/exam_form.html', context_data)


def examslist(request):
    ctx={}
    all_exams = Exams.objects.all()
    # print(all_exams)

    paginator = Paginator(all_exams, 10)
    page_number = request.GET.get('page')
    try:
        all_exam = paginator.page(page_number)
    except:
        all_exam = paginator.page(1)
    
    ctx['exams'] = all_exam

    return render(request, 'courses/exam_list.html',ctx)


@login_required(login_url = '/')
@custome_check()
def books(request):
    ctx={}
    ctx['course'] = Courses.objects.all().order_by('name')
    all_books = Books.objects.all().order_by('-id')

    paginator = Paginator(all_books, 10)
    page_number = request.GET.get('page')
    try:
        all_books = paginator.page(page_number)
    except:
        all_books = paginator.page(1)

    ctx['books'] = all_books

    return render(request,'courses/books_list.html',ctx)

def add_book(request):
    name = request.POST.get("book_name",None)
    cost = request.POST.get("book_cost",None)
    course_list = request.POST.getlist("book_course",None)
    book_content = request.FILES.get("book_content",None)
    
    course_list = ",".join(course_list)

    x = Books(
        name = name,
        cost = cost,
        course = course_list,
        book_content=book_content
    )
    x.save()

    return redirect(books)

def add_book_stock(request):
    newStock = request.POST.get("newStock",None)
    stock_book_id = request.POST.get("stock_book_id",None)

    if stock_book_id and newStock:
        Books.objects.filter(id=stock_book_id).update(
            stock = newStock,
        )

    return redirect(books)
