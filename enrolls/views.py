from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from enquiries.models import Enquiries, EnquiryCourses
from .models import Installments, PaymentMethod,PartnerPayment,SharedBooks
from datetime import datetime
from courses.models import Courses,Books
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime as dt
from anquira_v2 import anquira_handlers, choices
from django.views.generic import TemplateView
import datetime as new_dt
from datetime import timedelta
from .filters import EnrollmentFilter,FeesFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from users.models import CustomUserModel,PartnerPreferences
from django.shortcuts import redirect
from activity.views import log_activity
import json
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage
import csv
from django.http import HttpResponse, JsonResponse
from batches.models import Batches
from communication.views import send_refund_email,send_enrollment_email
from anquira_v2.decorators import custome_check
import csv


@login_required(login_url = '/')
@custome_check()
def enrollmentList(request):
    unroll=request.GET.get('unenroll_student',None)

    context_data={}
    request_data  = request.GET.copy()
    if not unroll:
        enrollments_obj = EnrollmentFilter(request_data, queryset=Enrollments.objects.all().order_by('-added_on')).qs
    else:
        strdt = new_dt.datetime.today().date() - timedelta(days=90)
        enddt = new_dt.datetime.today().date()
        enrollments_obj = EnrollmentFilter(request_data, queryset=Enrollments.objects.filter(added_on__gte=strdt, added_on__lte=enddt).order_by('-added_on')).qs

    
    sort_by = request.GET.get('sort_by',None)
    string = request.GET.get('string',None)
    if sort_by and string:
        if int(sort_by) == 1:
            enrollments_obj = Enrollments.objects.filter(enquiry_course_id__enquiry_id__full_name=string).order_by('-added_on')
        if int(sort_by) == 2:
            enrollments_obj = Enrollments.objects.filter(enquiry_course_id__enquiry_id__email=string).order_by('-added_on')
    
    # page = request.GET.get('page', 1)
    # page_data = Paginator(enrollments_obj, 10)
    # page_data.num_pages
    # try:
    #     data = page_data.page(page)
    # except PageNotAnInteger:
    #     data = page_data.page(1)
    # except EmptyPage:
    #     data = page_data.page(page_data.num_pages)
    # e_id = []
    eid = enrollments_obj.values_list('id', flat=True)
    # print(list(eid))
    # print(eid.count())

    if not unroll:
        paginator = Paginator(enrollments_obj, 10)
        page_number = request.GET.get('page')
        try:
            enrollments_obj = paginator.page(page_number)
        except:
            enrollments_obj = paginator.page(1)

    enrollments = []
    batch_obj = Batches.objects.all()
    for e_obj in enrollments_obj:
        values={}
        batch_obj = Batches.objects.filter(enroll_student = int(e_obj.id))
        enroll_status = None
        if batch_obj:
            enroll_status = True
        if unroll:
            if not batch_obj:
                values = {
                            'id': e_obj.id,
                            'full_name': e_obj.enquiry_course_id.enquiry_id.full_name,
                            # 'course': e_obj.enquiry_course_id.courses.name,
                            'discussed_fee': e_obj.discussed_fee,
                            # 'registration_amount': e_obj.registration_amount,
                            'pending_fee': e_obj.discussed_fee,
                            'registered_on': e_obj.registered_on,
                            'registered_by': e_obj.registered_by,
                            'enroll_courses':e_obj.enroll_courses,
                            'refund_amount':e_obj.refund_amount,
                            'refund':e_obj.refund,
                            'dropped':e_obj.dropped,
                            'certificate_issued':e_obj.certificate_issued,
                            'enroll_in_batch': enroll_status,
                            'enroll_type':e_obj.enroll_type,
                            'course_type':e_obj.course_type,
                        }
        else:
            values = {
                        'id': e_obj.id,
                        'full_name': e_obj.enquiry_course_id.enquiry_id.full_name,
                        # 'course': e_obj.enquiry_course_id.courses.name,
                        'discussed_fee': e_obj.discussed_fee,
                        # 'registration_amount': e_obj.registration_amount,
                        'pending_fee': e_obj.discussed_fee,
                        'registered_on': e_obj.registered_on,
                        'registered_by': e_obj.registered_by,
                        'enroll_courses':e_obj.enroll_courses,
                        'refund_amount':e_obj.refund_amount,
                        'refund':e_obj.refund,
                        'dropped':e_obj.dropped,
                        'certificate_issued':e_obj.certificate_issued,
                        'enroll_in_batch': enroll_status,
                        'enroll_type':e_obj.enroll_type,
                        'course_type':e_obj.course_type,
                    }
    
        if values:
            for inst in Installments.objects.filter(enrollmentid_id = e_obj.id, paid_unpaid=True):
                values['pending_fee'] -= inst.installment
        
            enrollments.append(values)

    context_data ={"enrollments": enrollments}
    context_data['users'] = CustomUserModel.objects.filter(exist_employee=True)
    context_data['courses'] = Courses.objects.all().order_by('name')
    context_data['q_courses'] = list(map(int, request.GET.getlist('course')))
    context_data['enrollments_obj'] = enrollments_obj
    context_data['eid'] = list(eid)
    return render(request, 'enrolls/enrollments_list.html', context_data)



@login_required(login_url = '/')
@custome_check()
def fees_view(request):
    students=Installments.objects.filter(paid_unpaid=False,fee_type=1).order_by('due_date').values('enrollmentid').distinct()

    name = request.GET.get("name",None)
    due_date_start = request.GET.get("due_date_start",None)
    due_date_end = request.GET.get("due_date_end",None)
    course = request.GET.get("course",None)
    batch = request.GET.get("batch",None)

    request.session['fees_filter_data']= None
    request.session['fees_filter_data'] = {'fees_name':name}
    request.session['fees_filter_data'] = {'due_date_start':due_date_start}
    request.session['fees_filter_data'] = {'due_date_end':due_date_end}
    request.session['fees_filter_data'] = {'course':course}
    request.session['fees_filter_data'] = {'batch':batch}


    if not name and not due_date_start and not due_date_end and  not course and not batch:
        request.session['fees_filter_data'] = ""

    context_data={}
    data  = request.GET.copy()
    q_courses=request.GET.getlist('course')
    data['course'] = ','.join(q_courses)
    
    q_batches=request.GET.getlist('batch')
    data['batch'] = ','.join(q_batches)

    # display all if unpaid
    #data['due_date_start'] = request.GET.get('due_date_start',datetime.today().strftime('%Y-%m-%d'))

    data['due_date_end'] = request.GET.get('due_date_end',(datetime.today()+ timedelta(days=365)).strftime('%Y-%m-%d'))
    
    students = FeesFilter(data, queryset=students).qs
    

    page = request.GET.get('page', 1)
    page_data = Paginator(students, 10)
    page_data.num_pages
    try:
        data = page_data.page(page)
    except PageNotAnInteger:
        data = page_data.page(1)
    except EmptyPage:
        data = page_data.page(page_data.num_pages)


    for student in data:
        enrolled_student=Enrollments.objects.get(pk=student.get('enrollmentid'))
        student['name'] = enrolled_student.enquiry_course_id.enquiry_id.full_name
        student['course']=enrolled_student.enquiry_course_id.courses.name
        student['batch'] = ''
        student['added_by'] = enrolled_student.registered_by.first_name
        pending_fee =enrolled_student.discussed_fee
        student['total_amount'] = pending_fee
        for inst in Installments.objects.filter(enrollmentid_id =enrolled_student, paid_unpaid=True):
            pending_fee -= inst.installment
        student['pending_fee'] = pending_fee
        today = datetime.now()
        next_installment_date = '-'
        next_installment = Installments.objects.filter(enrollmentid_id =enrolled_student, paid_unpaid=False).order_by('due_date').first()
        if next_installment:
            next_installment_date = next_installment.due_date.strftime( '%m/%d/%Y')
            student['is_overdue']=next_installment.due_date < today.date()
            student['installment'] = next_installment.installment
        student['next_due_date'] = next_installment_date
        
    context_data ={"students": data}
    context_data['q_courses']=list(map(int, q_courses))
    context_data['q_batches']=list(map(int, q_batches))

    context_data['courses'] = Courses.objects.all().order_by('name')
    context_data['batches']= Batches.objects.all().order_by('-start_date_time')
    return render(request, 'enrolls/fees_list.html', context_data)



@login_required(login_url = '/')
@custome_check()
@csrf_protect
def enrollment(request, enquiryid):
    ''' Note: enquiryid is not enquiry id --> it is Enquiry_Course_ID'''

    if int(enquiryid) == 1001:
        enroll_courses_list = request.POST.getlist("enroll_courses",None)
        
        if enroll_courses_list:
            enquiries_course = EnquiryCourses.objects.filter(id = int(enroll_courses_list[0])).first()
            enquiryid = enroll_courses_list
            enquiryid = (",").join(enquiryid)
        else:
            return redirect("/enquiries/list/")
    else:
        enquiries_course = EnquiryCourses.objects.filter(id = enquiryid).first() 
    
    enroll_courses_name = []
    if enquiryid:
        enqid = enquiryid.split(",")
        for i in enqid:
            a = Courses.objects.filter(id = int(i)).first()
            if a:
                enroll_courses_name.append(a.name)
            else:
                a = EnquiryCourses.objects.filter(id=int(i)).first()
                if a:
                    if a.courses.is_exam:
                        enroll_courses_name.append(a.courses.name+"(Exam)")
                    else:
                        enroll_courses_name.append(a.courses.name)

    context_data = {
        'enquiryid': enquiryid,
        'paymentMethod': PaymentMethod.objects.all(),
        'mindate':(datetime.now()- timedelta(days=6)).strftime( '%Y-%m-%d'),
        'maxdate':(datetime.now()+ timedelta(days=183)).strftime( '%Y-%m-%d'),
        'course': Courses.objects.all().order_by('name'),
        'enquiries_course':enquiries_course,
        'books':Books.objects.all(),
        'enroll_course_name':(",").join(enroll_courses_name),
    }
    
    # print("---------------------------------")
    # print(enquiryid)
    return render(request, 'enrolls/enrollsview.html', context_data)

@login_required(login_url = '/')
@custome_check()
@csrf_exempt
def enrollsview(request, enrollment_id):
   
    if request.method == "POST":
        installment_value = request.POST['installments']
        due_date_value = request.POST['duedate']
        payment_method_id = request.POST['payment_method']
        comment = request.POST['comment']
        enrolls = Enrollments.objects.get(id = int(enrollment_id))
        installmentNumber = Installments.objects.filter(enrollmentid_id = enrolls.id).count()
        Installments.objects.create(enrollmentid_id = int(enrollment_id), installment = installment_value,\
             due_date = due_date_value, installment_no = installmentNumber + 1,\
             payment_method_id = int(payment_method_id),comment=comment)
    enrollments = Enrollments.objects.get(id = enrollment_id)
    installments = Installments.objects.filter(enrollmentid = enrollment_id)
    enquiry_course = EnquiryCourses.objects.filter(id=enrollments.enquiry_course_id.id).first()
    installment_sum = Installments.objects.filter(enrollmentid_id = enrollment_id).aggregate(Sum('installment'))
    # print(installment_sum['installment__sum'])
    # print(type(installment_sum))
    
    enroll_courses_name = []
    if enrollments.enroll_courses:
        enroll_cou = enrollments.enroll_courses
        enroll_cou = enroll_cou.split(",")
        for i in enroll_cou:
            # print(i)
            a = Courses.objects.filter(id = int(i)).first()
            if a:
                enroll_courses_name.append(a.name)
            else:
                a = EnquiryCourses.objects.filter(id=int(i)).first()
                if a:
                    print("==================================**********************************==========================================")
                    print(a.courses.is_exam)
                    if a.courses.is_exam:
                        enroll_courses_name.append(a.courses.name+"(Exam)")
                    else:
                        enroll_courses_name.append(a.courses.name)

    context_data = {
        "enrollments": enrollments,
        'installments': Installments.objects.filter(enrollmentid_id = enrollment_id),
        'paymentMethod': PaymentMethod.objects.all(),
        'mindate':(datetime.now()- timedelta(days=6)).strftime( '%Y-%m-%d'),
        'maxdate':(datetime.now()+ timedelta(days=183)).strftime( '%Y-%m-%d'),
        'course': Courses.objects.all().order_by('name'),
        'enquiries_course':enquiry_course,
        'edit':'yes',
        'installments_count': Installments.objects.filter(enrollmentid_id = enrollment_id).count(),
        'installment_sum':installment_sum,
        'installment_sum':installment_sum,
        'partner_payment': PartnerPayment.objects.filter(enrollment = enrollments.id),
        'partner':PartnerPreferences.objects.all(),
        'books':Books.objects.all(),
        'shared_books':SharedBooks.objects.filter(enrollments=enrollment_id),
        'enquiryid':enrollments.enroll_courses,
        'enroll_course_name':(",").join(enroll_courses_name),
        'exam_fee':enrollments.exam_share,
        'book_fee':enrollments.book_share,
        'vandor_fee':enrollments.vandor_share,
        'other_fee':enrollments.other_share,
        'ap2v_fee':round(enrollments.ap2v_share,2),
        

    }
    return render(request, 'enrolls/enrollsview.html', context_data)


@login_required(login_url = '/')
@custome_check()
def paidInstallment2(request):
    if request.method == "POST" and request.FILES['payment_file']:
        # instalmentdata = Installments.objects.get(id = paid_id)
        # print(request)
        installment_row = request.POST.get("installment_row2",None)
        payment_method = request.POST.get("paymentMethod",None)
        enrollment_id = request.POST.get("enrollment_id",None)
        payment_file = request.FILES['payment_file']

        if installment_row and payment_method and payment_file:
            from datetime import date
            fs = FileSystemStorage()
            file = fs.save(payment_file.name, payment_file)
            fileurl = fs.url(file)
            instalmentdata = Installments.objects.get(id = installment_row)

            instalmentdata.paid_unpaid = True
            instalmentdata.payment_method_id = int(payment_method)
            instalmentdata.attachment = payment_file
            instalmentdata.paid_on = date.today()
            instalmentdata.save()

        return redirect('enrollment_view',enrollment_id=enrollment_id)
    

@login_required(login_url = '/')
@custome_check()
def enroll_search(request):
    results = []
    if "course_id" in request.GET and "query" in request.GET:
        course_id = request.GET['course_id']
        s_string = request.GET['query']
        ### serach syntax in fastselect api.
        # results = [
        # 	{"text": "Afghanistan", "value": "Afghanistan"},
        # 	{"text": "Albania", "value": "Albania"},
        # 	{"text": "Algeria", "value": "Algeria"},
        # 	{"text": "Angola", "value": "Angola"}
        # ]
        if s_string != "":
            if s_string[0] in "0123456789":
                e_objs = Enrollments.objects.filter(enquiry_course_id__enquiry_id__mobile__istartswith = s_string, enquiry_course_id__courses__id = int(course_id))
                for e_obj in e_objs:
                    text = "{} ({})".format(e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile)
                    value = e_obj.id
                    results.append({"text": text, "value": value})
            else:
                e_objs = Enrollments.objects.filter(enquiry_course_id__enquiry_id__full_name__istartswith = s_string, enquiry_course_id__courses__id = int(course_id))
                for e_obj in e_objs:
                    text = "{} ({})".format(e_obj.enquiry_course_id.enquiry_id.full_name, e_obj.enquiry_course_id.enquiry_id.mobile)
                    value = e_obj.id
                    results.append({"text": text, "value": value})
        else:
            pass
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse(results, safe=False)

class TodoInstallmentTemplateView(TemplateView):
    template_name = "enrolls/todo_installment.html"
    model = Installments

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_installments'] = self.model.objects.filter(
            due_date=new_dt.date.today(),
            # due_date__gte=new_dt.date.today() + timedelta(days=1),
            paid_unpaid=False
        )
        return context

class ViewInstallmentTemplateView(TemplateView):
    template_name = "enrolls/view_installment.html"
    model = Installments

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        installment_obj = self.model.objects.filter(id=self.kwargs.get('pk'))
        if installment_obj.exists():
            context['installment_data'] = installment_obj.first()
        return context

    def post(self, *args, **kwargs):
        from django.urls import reverse_lazy
        response = {'status': 1}

        obj = self.model.objects.filter(id=self.kwargs.get('pk'))
        if obj.exists():
            redirect_url = reverse_lazy(
                'enrollment_view',
                kwargs={'enrollment_id': obj.first().enrollmentid_id})

            response['redirect'] = redirect_url

            due_date = datetime.strptime(self.request.POST.get('due_date'), '%m/%d/%Y')

            obj.update(
                installment=self.request.POST.get('installment'),
                due_date=due_date,
            )
        else:
            response.update(status=0)

        return JsonResponse(response)

def update_enrolment(request):
    if request.method == "POST":
        # print("------------7-------------")
        enrolment_name = request.POST['enquiry_id']
        # enrollcourse = request.POST['enrollcourse']
        enrollcourse = ",".join(request.POST.getlist('enrollcourse'))
        discuss_fee = request.POST['discuss_fee']
        # registration_amount = request.POST['registration_amount']
        registered_on = request.POST['registered_on']
        registered_by = request.POST['registered_by']
        added_on = request.POST['added_on']
        e_id = request.POST['e_id']
        # print(enrollcourse)
        try:
            if e_id:
                e = Enrollments.objects.filter(id = e_id).first()

                ec = EnquiryCourses.objects.filter(id = e.enquiry_course_id.id).first()

                Enquiries.objects.filter(id=ec.enquiry_id.id).update(
                    full_name = enrolment_name
                )
                print("---",e.enquiry_course_id.id)
                try:
                    EnquiryCourses.objects.filter(id = e.enquiry_course_id.id).update(
                        courses = enrollcourse
                    )
                except Exception as e:
                    print(e)

                
                Enrollments.objects.filter(id = e_id).update(
                    discussed_fee = discuss_fee,
                    # registration_amount = registration_amount,
                    # registered_by = request.POST['registered_by']
                    enroll_courses = enrollcourse
                )
                if registered_on:
                    Enrollments.objects.filter(id = e_id).update(
                        registered_on = registered_on,
                    )
                if added_on:
                    Enrollments.objects.filter(id = e_id).update(
                        added_on = added_on
                    )
                page = '/enrollments/enrollment_view/'+e_id

                try:
                    log_activity(request,action=choices.Action.mod_enrollment, action_detail=choices.ActionDetails.mod_enrollment,id=e_id)
                except Exception as e:
                    print(e)
                return redirect (page)
            else:
                return redirect ('list')
        except Exception as e:
            print(e)
            return redirect ('list')


def save_enroll_data(request):
    data={}
    # print("-----------------SAVE ENROLL DATA FUNCTION----------------------------")
    installment = request.GET.get("enrollments",None)
    update_installment = request.GET.get("update_enrollment",None)
    enroll_course_id = request.GET.get("enroll_course_id")
    courses = request.GET.get("course")
    discussed_fee = request.GET.get("discussed_fee")
    enroll_type = request.GET.get("enroll_type")
    exam_fee_h = request.GET.get("exam_fee_h")
    book_fee_h = request.GET.get("book_fee_h")
    vandor_fee_h = request.GET.get("vandor_fee_h")
    ap2v_fee_h = request.GET.get("ap2v_fee_h")
    current_h = request.GET.get("current_h")
    recive_h = request.GET.get("recive_h")
    other_fee_h = request.GET.get("other_fee_h")
    # print('pqqqaashish'*100)
    # print(recive_h)
    # print('this ecxam',exam_fee_h)
    # print('this book',book_fee_h)
    # print('this ap2v share',ap2v_fee_h)
    # print('this other share',other_fee_h)

    
    
    print("--------------------------------123456789---------------------------------------------------------------------")
    print(enroll_type)
    

    enquiry_id = EnquiryCourses.objects.filter(id = enroll_course_id).first()
    enquiry_id = enquiry_id.enquiry_id.id

    courses = json.loads(courses)
    courses = courses.split(",")
    # courses = ",".join(courses)

    all_enroll_courses = (",").join(courses)

    discussed_fee_gst = (int(discussed_fee)*18)/100
    print(discussed_fee_gst)

    for i in courses:
        print(i)
        print(EnquiryCourses.objects.get(id = int(i)))
        if Enrollments.objects.filter(enquiry_course_id = int(i)).exists():
            x = Enrollments.objects.filter(enquiry_course_id = EnquiryCourses.objects.get(id = int(i))).update(
                discussed_fee = discussed_fee,
                discussed_fee_gst = discussed_fee_gst,
                enroll_courses = all_enroll_courses, 
                ap2v_share_recived=current_h,
                current_recived_amount=recive_h,
                exam_share=exam_fee_h,
                book_share=book_fee_h,
                vandor_share=vandor_fee_h,
                ap2v_share=ap2v_fee_h,
                other_share=other_fee_h
                # payment_method_id = 1,
                # registration_amount = 0,
                # registered_by_id = request.user.id,
            )
            x = Enrollments.objects.filter(enquiry_course_id =int(i)).first()
        else:
            x = Enrollments(
                discussed_fee = discussed_fee,
                discussed_fee_gst = discussed_fee_gst,
                enroll_courses = all_enroll_courses,
                enquiry_course_id = EnquiryCourses.objects.get(id = int(i)),
                payment_method_id = 1,
                # registration_amount = 0,
                registered_by_id = request.user.id,
                enroll_type=enroll_type,
                exam_share=exam_fee_h,
                book_share=book_fee_h,
                vandor_share=vandor_fee_h,
                other_share=other_fee_h,
                ap2v_share=ap2v_fee_h,
                ap2v_share_recived=current_h,
                current_recived_amount=recive_h

                )
            x.save()
        break

    
    if installment:
        installment = json.loads(installment)
        number = 1
        for i in installment:
            y = Installments(
                installment_no  = number,
                installment = i['installment'],
                due_date = i['datetimepicker'],
                comment = i['comment'],
                paid_unpaid = int(i['paid']),
                enrollmentid_id = x.id,
                payment_method_id = 1,
                attachment=i['screenshot']
            )

            if int(i['paid']) == True:
                from datetime import date
                y.paid_on = date.today()

            y.save()
            number=number+1

    
    if update_installment:
        update_installment = json.loads(update_installment)
        # print(update_installment)
        for j in update_installment:
            Installments.objects.filter(id = j['row']).update(
                installment = j['installment'],
                due_date = j['datetimepicker'],
                comment = j['comment'],
            )
    
    for i in courses:
        EnquiryCourses.objects.filter(id = int(i)).update(
            status = 1
        )
    
    new_enroll = request.GET.get("new",None)
    if new_enroll:
        try:
            course_list = []
            send_email_course = None
            for i in courses:
                enroll_c = EnquiryCourses.objects.get(id = int(i)).courses.name
                course_list.append(enroll_c)
                enroll_course_type = EnquiryCourses.objects.get(id = int(i)).courses.typee
                if enroll_course_type==1:
                    send_email_course = True
            join_course_name = (" and ").join(course_list)
            email = Enrollments.objects.filter(id=x.id).first().enquiry_course_id.enquiry_id.email
            if email:
                password=None
                if not CustomUserModel.objects.filter(email=email).exists():
                    # print("User Not Found")
                    enroll_obj2 = Enrollments.objects.filter(id=x.id).first()
                    name = enroll_obj2.enquiry_course_id.enquiry_id.full_name
                    password_name = name.split(" ")
                    password_number = enroll_obj2.enquiry_course_id.enquiry_id.mobile
                    if password_number:
                        password_number = password_number[-4:]
                    else:
                        password_number = 3691
                    password = str(password_name[0])+"@"+str(password_number)
                    username_email = email.replace("@",'.')
                    save_user = CustomUserModel.objects.create(
                        first_name = name,
                        username = username_email,
                        email = email.lower(),
                        user_type = 'student',
                        is_verified = False, 
                    )
                    save_user.set_password(password)
                    save_user.save()
                    # print("User created with : ",password)
                
                
                if send_email_course:
                    print("Sending mail...")
                    send_enrollment_email(request,join_course_name,email,password)    
                # print("Mail Sended") 

        except Exception as e:
            print(e)
    return JsonResponse(data)


def partner_payment_add(request):
    if request.method == "POST":
        enrollment_id = request.POST.get("enrollment_id",None)
        partner = request.POST.get("partner",None)
        amount = request.POST.get("amount",0)
        paid_on = request.POST.get("paid_on",None)
        is_paid = request.POST.get("is_paid",False)
        if is_paid:
            is_paid = True
        if paid_on =="" or paid_on == " ":
            paid_on = None


        x = PartnerPayment(
            partner = PartnerPreferences.objects.get(id=partner),
            enrollment = Enrollments.objects.get(id=enrollment_id),
            amount = amount,
            is_paid = is_paid,
            paid_on = paid_on,
            added_by = request.user,
        )
        x.save()

    return redirect('enrollment_view',enrollment_id=enrollment_id)

def update_partnet_data_section(request):
    ctx={}
    id = request.GET.get("id",None)
    # print(id)
    if id:
        partner_queryset = PartnerPayment.objects.filter(id=id).first()
        ctx['partner_queryset']=partner_queryset
        ctx['partner']=PartnerPreferences.objects.all()
        # print(ctx['partner'])
    return render(request,'enrolls/update_partner_payment.html',ctx)


def partner_payment_update(request):
    data={}
    if request.method == "POST":
        amount = request.POST.get("update_amount",0)
        paid_on = request.POST.get("update_paid_on",None)
        is_paid = request.POST.get("update_is_paid",False)
        partner_payment_row = request.POST.get("partner_payment_id",None)
        if is_paid:
            is_paid = True
        if paid_on =="" or paid_on == " ":
            paid_on = None

        if partner_payment_row:
            PartnerPayment.objects.filter(id = partner_payment_row).update(
                amount = amount,
                is_paid = is_paid,
                paid_on = paid_on,
                updated_by = request.user,
            )
        enrollment_id = PartnerPayment.objects.filter(id = partner_payment_row).first().enrollment
    return redirect('enrollment_view',enrollment_id=enrollment_id.id)


def download_excel(request):
    fees_queryset = Installments.objects.filter(paid_unpaid=False, enrollmentid__batch__isnull = False).order_by('due_date')


    if request.session['fees_filter_data']:
        if request.session['fees_filter_data']['name']:
            fees_queryset = fees_queryset.filter(enrollmentid__enquiry_course_id__enquiry_id__full_name__icontains = request.session['fees_filter_data']['name'])
        if request.session['fees_filter_data']['due_date_start']:
            fees_queryset = fees_queryset.filter(due_date_start = request.session['fees_filter_data']['due_date_start'])
        if request.session['fees_filter_data']['due_date_end']:
            fees_queryset = fees_queryset.filter(email = request.session['fees_filter_data']['email'])
        if request.session['fees_filter_data']['course']:
            fees_queryset = fees_queryset.filter(enrollmentid__enquiry_course_id__courses__in = request.session['fees_filter_data']['course'].split(','))
        if request.session['fees_filter_data']['batch']:
            fees_queryset = fees_queryset.filter(enrollmentid__batch__batch_name__icontains = request.session['fees_filter_data']['batch'])
        
    
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['SrNo','Name','Course','Batch','Pending Fee','Total Amount','Next Due Date'])

    for i in fees_queryset:
        row = (
            i.id,
            i.enrollmentid.enquiry_course_id.enquiry_id.full_name,
            i.enrollmentid.enquiry_course_id.courses.name,
            i.enrollmentid.batch.batch_name,
            i.enrollmentid.discussed_fee,
            i.installment,
            i.due_date,
        )
        writer.writerow(row)

    response['Content-Disposition'] = 'attachment; filename=Enquires-{date}.csv'.format(date=datetime.now().strftime('%d-%m-%Y'),)
    return response
    # return HttpResponse("ok")


def download_pdf(request, *args, **kwargs):
    enquires_queryset = Enquiries.objects.all()

    if request.session['enquiry_filter_data']:
        if request.session['enquiry_filter_data']['name']:
            enquires_queryset = enquires_queryset.filter(full_name = request.session['enquiry_filter_data']['name'])
        if request.session['enquiry_filter_data']['mobile']:
            enquires_queryset = enquires_queryset.filter(mobile = request.session['enquiry_filter_data']['mobile'])
        if request.session['enquiry_filter_data']['email']:
            enquires_queryset = enquires_queryset.filter(email = request.session['enquiry_filter_data']['email'])
        if request.session['enquiry_filter_data']['reference']:
            enquires_queryset = enquires_queryset.filter(reference = request.session['enquiry_filter_data']['reference'])
        if request.session['enquiry_filter_data']['start_date']:
            sd = request.session['enquiry_filter_data']['start_date']+" 00:00:00"
            sd = datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
            enquires_queryset = enquires_queryset.filter(added_on__gte = sd)
        if request.session['enquiry_filter_data']['end_date']:
            ed = request.session['enquiry_filter_data']['end_date']+" 00:00:00"
            ed = datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")
            enquires_queryset = enquires_queryset.filter(added_on__lte = ed)
        if request.session['enquiry_filter_data']['training_mode']:
            enquires_queryset = enquires_queryset.filter(training_mode = request.session['enquiry_filter_data']['training_mode'])
        if request.session['enquiry_filter_data']['discarded']:
            enquires_queryset = enquires_queryset.filter(tmp_discard = request.session['enquiry_filter_data']['discarded'])

    pdf = render_to_pdf('enquiries/pdfgen.html', {'enquires_queryset':enquires_queryset})
    return HttpResponse(pdf, content_type='application/pdf')

def shared_book_add(request):
    book = request.POST.get("shared_book",None)
    enrollment_id = request.POST.get("enrollment_id",None)

    x = SharedBooks(
        enrollments = Enrollments.objects.get(id=enrollment_id),
        book = Books.objects.get(id=book),

    )
    x.save()
    return redirect("view/"+enrollment_id)

def update_book(request):
    data={}
    shared_book_id = request.GET.get("id",None)
    if shared_book_id:
        book_id = SharedBooks.objects.filter(id=shared_book_id).first().book.id
        book_obj = Books.objects.filter(id = book_id).first()
        if book_obj.stock > 0:
            SharedBooks.objects.filter(id=shared_book_id).update(
                is_shared = True
            )

            Books.objects.filter(id = book_id).update(
                stock = int(book_obj.stock)-1
            )
            data['code'] = 200
        else:
            data['code'] = 201
    return JsonResponse(data)

def save_attachment(request):
    data={}
    attachment = request.FILES.get("file")
    if attachment:
        fs = FileSystemStorage()
        import uuid
        a=uuid.uuid4()
        a=str(a)
        file = fs.save(attachment.name, attachment)
        # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        fileurl = fs.url(file)

        x = Screenshot(
            attachment = attachment
        )
        x.save()
        a = str(x.attachment)
        data['name'] = a
    return JsonResponse({"name":a})

def refund_payment(request):
    data={}
    amount = request.POST.get("amount",None)
    date = request.POST.get("date",None)
    reason = request.POST.get("reason",None)
    refund_enrollment_id = request.POST.get("refund_enrollment_id",None)
    payment_file = request.FILES['file']

    if refund_enrollment_id and amount and date and payment_file and reason:
        fs = FileSystemStorage()
        file = fs.save(payment_file.name, payment_file)
        fileurl = fs.url(file)

        x = Installments(
            enrollmentid = Enrollments.objects.filter(id = int(refund_enrollment_id)).first(),
            payment_method_id = 1,
            installment_no = 0,
            installment = amount,
            comment = reason,
            paid_unpaid = 1,
            added_on = date,
            attachment = payment_file,
            fee_type = 2,
            due_date = date
        )
        x.save()

        Enrollments.objects.filter(id=int(refund_enrollment_id)).update(
            refund=True,
            dropped=True,
            dropped_on=dt.today(),
            refund_amount = amount
        )

        installment_obj = Installments.objects.filter(enrollmentid = refund_enrollment_id,paid_unpaid=False)
        for i in installment_obj:
            Installments.objects.filter(id = i.id).update(
                fee_type = 3                            # mark as cancel
            )


        enroll_name = Enrollments.objects.filter(id = int(refund_enrollment_id)).first().enquiry_course_id.enquiry_id.full_name
        try:
            send_refund_email(request,enroll_name,refund_enrollment_id,amount,date)
        except Exception as e:
            print(e)
        data["status"] = 200
    else:
        data["status"] = 401
        data["message"] = "All filed are fields are compulsory"
    return JsonResponse(data)

def drop_student(request):
    data={}
    enrollment_id=request.POST.get("enrollments_id",None)
    print(enrollment_id)
    if enrollment_id:
        Enrollments.objects.filter(id = int(enrollment_id)).update(
            dropped=True,
            dropped_on=dt.today()
        )

        installment_obj = Installments.objects.filter(enrollmentid = int(enrollment_id),paid_unpaid=False)
        for i in installment_obj:
            Installments.objects.filter(id = i.id).update(
                fee_type = 3                            # mark as cancel
            )

        data["status"] = 200
    else:
        data["status"] = 401
        data["message"] = "Something went wrong!!!"
    return JsonResponse(data)

def rejoin_student(request):
    data={}
    enrollment_id=request.POST.get("enrollments_id",None)
    print(enrollment_id)
    if enrollment_id:
        Enrollments.objects.filter(id = int(enrollment_id)).update(
            dropped=False,
            dropped_on=None
        )

        installment_obj = Installments.objects.filter(enrollmentid = int(enrollment_id),paid_unpaid=False)
        for i in installment_obj:
            Installments.objects.filter(id = i.id).update(
                fee_type = 1                            # mark as cancel
            )

        data["status"] = 200
    else:
        data["status"] = 401
        data["message"] = "Something went wrong!!!"
    return JsonResponse(data)

def enrollmentsCSV(request):
    # print(request.body)
    context_data={}
    # request_data  = request.GET.copy()
    # enrollments_obj = EnrollmentFilter(request_data, queryset=Enrollments.objects.all().order_by('-added_on')).qs
    enroll_id = request.GET.get("enroll_id",None)
    # print(enroll_id)
    # print(type(enroll_id))

    enroll_id = enroll_id.replace('[','')
    enroll_id = enroll_id.replace(']','')
    enroll_id = enroll_id.split(",")
    enroll_id = [int(i) for i in enroll_id]

    enrollments_obj = Enrollments.objects.filter(id__in=enroll_id)

    # print(enroll_id)
    # print(type(enroll_id))
    # print("********************************************************************************************************************************************************************************")
    # print(enrollments_obj)
    # print(enrollments_obj.count())

    

    sort_by = request.GET.get('sort_by',None)
    string = request.GET.get('string',None)
    if sort_by and string:
        if int(sort_by) == 1:
            enrollments_obj = Enrollments.objects.filter(enquiry_course_id__enquiry_id__full_name=string).order_by('-added_on')
        if int(sort_by) == 2:
            enrollments_obj = Enrollments.objects.filter(enquiry_course_id__enquiry_id__email=string).order_by('-added_on')

    enrollments = []
    for e_obj in enrollments_obj:
        values = {
                    'id': e_obj.id,
                    'full_name': e_obj.enquiry_course_id.enquiry_id.full_name,
                    'mobile': e_obj.enquiry_course_id.enquiry_id.mobile,
                    'email': e_obj.enquiry_course_id.enquiry_id.email,
                    # 'course': e_obj.enquiry_course_id.courses.name,
                    'discussed_fee': e_obj.discussed_fee,
                    # 'registration_amount': e_obj.registration_amount,
                    'pending_fee': e_obj.discussed_fee,
                    'registered_on': e_obj.registered_on,
                    'registered_by': e_obj.registered_by,
                    'enroll_courses':e_obj.enroll_courses,
                    'refund_amount':e_obj.refund_amount,
                    'refund':e_obj.refund,
                    'dropped':e_obj.dropped,
                    'certificate_issued':e_obj.certificate_issued,
                }
        for inst in Installments.objects.filter(enrollmentid_id = e_obj.id, paid_unpaid=True):
            values['pending_fee'] -= inst.installment
        enrollments.append(values)
    context_data ={"enrollments": enrollments}

    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['SrNo','Id','Name','mobile','email','Course','Discuss Fee','Pending Fee','Register on','Register By'])

    n = 1
    for i in enrollments:
        enrl_course = []
        try:
            enrol_course_id = i['enroll_courses'].split(",")
            for m in enrol_course_id:
                enq_cour_obj = EnquiryCourses.objects.filter(id=int(m)).first()
                if enq_cour_obj:
                    enrl_course.append(enq_cour_obj.courses.name)
        except Exception as e:
            print(e)
        
        u_name = i['registered_by']
        user_obj = CustomUserModel.objects.filter(username=u_name).first()
        if user_obj:
            u_name = user_obj.first_name

        row = (
            n,
            i['id'],
            i['full_name'],
            i['mobile'],
            i['email'],
            enrl_course,
            i['discussed_fee'],
            i['pending_fee'],
            i['registered_on'],
            u_name,
        )
        n=n+1
        writer.writerow(row)

    response['Content-Disposition'] = 'attachment; filename=EnrollmentData-{date}.csv'.format(date=datetime.now().strftime('%d-%m-%Y'),)
    return response
    # return HttpResponse("ok")


def send_enroll_mail_again(request):
    data={}
    enroll_id = request.GET.get("enroll_id",None)

    enroll_obj2 = Enrollments.objects.filter(id=enroll_id).first()
    email = enroll_obj2.enquiry_course_id.enquiry_id.email

    if not CustomUserModel.objects.filter(email=email).exists():
        enroll_obj2 = Enrollments.objects.filter(id=enroll_id).last()
        name = enroll_obj2.enquiry_course_id.enquiry_id.full_name
        password_name = name.split(" ")
        password_number = enroll_obj2.enquiry_course_id.enquiry_id.mobile
        if password_number:
            password_number = password_number[-4:]
        else:
            password_number = 3691
        password = str(password_name[0])+"@"+str(password_number)
        username_email = email.replace("@",'.')
        save_user = CustomUserModel.objects.create(
            first_name = name,
            username = username_email,
            email = email.lower(),
            user_type = 'student',
            is_verified = False, 
        )
        save_user.set_password(password)
        save_user.save()
    else:
        enroll_obj2 = Enrollments.objects.filter(id=enroll_id).last()
        name = enroll_obj2.enquiry_course_id.enquiry_id.full_name
        password_name = name.split(" ")
        password_number = enroll_obj2.enquiry_course_id.enquiry_id.mobile
        if password_number:
            password_number = password_number[-4:]
        else:
            password_number = 3691
        password = str(password_name[0])+"@"+str(password_number)
        cx = CustomUserModel.objects.filter(email=email).first()
        cx.set_password(password)
        cx.save()

    
    course_list = []
    send_email_course = None
    course = enroll_obj2.enroll_courses.split(",")
    for i in course:
        enroll_c = EnquiryCourses.objects.get(id = int(i)).courses.name
        course_list.append(enroll_c)
        enroll_course_type = EnquiryCourses.objects.get(id = int(i)).courses.typee
        if enroll_course_type==1:
            send_email_course = True

    join_course_name = (" and ").join(course_list)
    if send_email_course:
        print("Sending mail...")
        send_enrollment_email(request,join_course_name,email,password)
    return JsonResponse(data)

def check_student_enrolled_batches(request):
    ctx={}
    enroll_id = request.GET.get("enroll_id",None)
    print(enroll_id)

    if enroll_id:
        batch_obj = Batches.objects.filter(enroll_student = enroll_id)
        print(batch_obj)
        # for i in batch_obj:
        #     print(i.batch_name)
        ctx['batch_obj'] = batch_obj
    return render(request,"enrolls/enrolled_batches.html",ctx)


def create_revision_enrollment(request):
    old_enrollment_id = request.GET.get("enrollment_id",None)
    print(old_enrollment_id)
    if old_enrollment_id:
        enrollment_obj = Enrollments.objects.filter(id=old_enrollment_id).last()
        if enrollment_obj:

            x = Enrollments(
                discussed_fee = 0,
                enroll_courses = enrollment_obj.enroll_courses,
                enquiry_course_id = enrollment_obj.enquiry_course_id,
                payment_method_id = 1,
                # registration_amount = 0,
                registered_by_id = request.user.id,
                enroll_type=2,
                parent_enrollment_id = old_enrollment_id
                )
            x.save()

            print(x.id)
    return redirect("list")