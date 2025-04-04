from django import template
from demo.models import Demo,DemoSaveVideo
from ap2v_courses.models import City_Specific_Course, Courses, Offers,Industry_Projects
from home.models import Category
from batches.models import Batches,BestRecording,CompleteRecording
from courses.models import Courses as Anquira_courses
register = template.Library()
from enquiries.models import EnquiryCourses,Followups
from testimonials.models import Text
from datetime import datetime, timedelta
from landing_page.models import Landing_Page
import datetime
import re
from enrolls.models import Enrollments
from users.models import CustomUserModel as User
from django.db.models import Q
from django.conf import settings
from blogs.models import InterviewQuestionTitleDescription
from recording_sessions.models import Recorded_Courses_name
from learning_paths.models import Learning_Path,Learning_Path_Courses


@register.filter(name='get_tags_by_event_id')
def get_tags_by_event_id(offer_id):
	uniq_tags = []
	offer_obj = Offers.objects.get(id=offer_id)
	for course in offer_obj.courses.all():
		for tag in course.tags.all():
			if tag.name not in uniq_tags:
				uniq_tags.append(tag.name)
	return uniq_tags

@register.filter(name="discount_in_price")
def discount_in_price(total_price, discount_price):
        #percentage_cal = price - ((int(price)*40)/ 100)
        if total_price !=0:
            percentage_cel = (float(total_price-discount_price)/total_price) * 100
            return int(percentage_cel)
        return 0
@register.filter(name="replace_space_in_tag")
def replace_space_in_tag(tag_string):
    tag_string=str(tag_string)
    if " " in tag_string:
        return tag_string.replace(" ", "-")
    else:
        return tag_string

@register.filter(name="get_offer_courses_object")
def get_offer_courses_object(course_offer):
        a = 0
        for course in course_offer:
            a += int(course.price)
        return a


@register.simple_tag
# @register.filter(name="get_courses_on_tab_home")
def get_courses_on_tab_home(course):
    category_obj = Category.objects.filter(slug='course')
    development_courses = Courses.objects.filter(category_name = category_obj.first(),active_inactive=True)
    return development_courses

@register.simple_tag
def get_name(name):
    return "Neeraj"

@register.simple_tag
def get_category_course(category):
    # print(category)
    category_obj = Category.objects.filter(slug=category)
    category_courses = Courses.objects.filter(category_name = category_obj.first(),active_inactive=True)
    # print(category_courses)
    return category_courses

@register.simple_tag
def get_city_category_course(category=None,city_name=None):
    # print("-=-----------###############################################")
    print(category)
    print(city_name)
    category_obj = Category.objects.filter(slug=category).first()
    # category_courses = City_Specific_Course.objects.filter(city__name=city_name,course__category_name=category_obj)
    # print(category_courses)
    if category and city_name:
        category_courses = City_Specific_Course.objects.filter(city__name=city_name,course__category_name=category_obj)
    elif category:
        category_courses = Courses.objects.filter(category_name = category_obj,active_inactive=True)
    return category_courses

@register.simple_tag
def is_vowel(word):
    # vowel alphabet
    vowel = 'aeiou'

    if word[0].lower() in vowel:
        return True

    return False


@register.simple_tag
def get_city_course(city):
    # print(city)
    city_course_obj = City_Specific_Course.objects.filter(city=city)
    # print(city_course_obj)
    return city_course_obj

@register.simple_tag
def get_chat_room_title(uuid=None):
    if uuid:
        batch_obj = Batches.objects.filter(chat_room_id=uuid).last()
        if batch_obj:
            for  i in batch_obj.courses.all():
                return i
        else:
            return uuid

@register.simple_tag
def get_chat_room_id(uuid=None):
    if uuid:
        batch_obj = Batches.objects.filter(chat_room_id=uuid).last()
        if batch_obj:
            return batch_obj
        else:
            return "N/A"

@register.simple_tag
def get_book_courses(course_id=None):
    # print(course_id)
    course_id = course_id.split(",")
    # print(course_id)
    course_list = []
    for i in course_id:
        course_obj = Anquira_courses.objects.filter(id = int(i)).first()
        course_list.append(course_obj.name)
    all_course = ', '.join(course_list)
    return all_course

@register.simple_tag
def get_skill(skills):
    # print(skills)
    try:
        skill_point = skills.split(",")
    except:
        skill_point = ['N/A','N/A']
    # skill_point = ['DevOps methodologies', 'Version control systems', 'Jenkins TeamCity Maven', 'Continuous integration and deployment']
    return skill_point

@register.simple_tag
def get_landing_page_course_project(course_id):
    project_obj = None
    # print(course_id)
    if course_id:
        project_obj = Industry_Projects.objects.filter(belong_course = course_id)
        # print(project_obj)
    return project_obj

@register.simple_tag
def get_batch_courses(batch_id):
    if batch_id:
        batch_obj = Batches.objects.filter(id = batch_id).first()
        if batch_obj:
            course_list = []
            for j in batch_obj.courses.all():
                course_list.append(j.name)
            return " and ".join(course_list)
    return "N/A"

@register.simple_tag
def filter_number(number):
    # print(number)
    return "N/A"

# @register.simple_tag
# def enquiries_filter(enquiry_id):
#     print(enquiry_id)
#     enq_course_obj = EnquiryCourses.objects.filter(enquiry_id = enquiry_id)
#     status_list = []
#     for i in enq_course_obj:
#         print("       Status: ",i.status)
#         status_list.append(int(i.status))
    
#     if 2 in status_list and 1 in status_list:
#         return "no"
#     else:
#         return "yes"

@register.simple_tag
def get_landing_page_course_testimonials(course_id):
    project_obj = None
    # print(course_id)
    if course_id:
        project_obj = Text.objects.filter(course = course_id)
        # print(project_obj)
    return project_obj

@register.simple_tag
def get_batch_student_count(batch_id):
    batch_student_count = '--'
    # print(batch_id)
    if batch_id:
        batch_obj = Batches.objects.filter(id=batch_id).first()
        batch_student_count = batch_obj.enroll_student.all().count()
    return batch_student_count


@register.simple_tag
def get_start_date(lp_id):
    # landing_page_start = Landing_Page.objects.filter(id = lp_id).first().start_date
    landing_page_start = datetime.datetime.now()+timedelta(days=7)
    return landing_page_start


@register.simple_tag
def check_remaning_batch_day(end_date):
    batch_end = None
    print('--'*50)
    print(end_date.date())
    # end_date = end_date
    from datetime import timedelta, date
    EndDatePlus = date.today() + timedelta(days=10)
    print(EndDatePlus)
    today_date = date.today()
    diff = end_date.date()-today_date
    print(diff.days)
    if EndDatePlus >= end_date.date():
        batch_end = True
        # print("TYREEEEEEEEEEE")
        # print(end_date.date()-date.today())
        # batch_end = end_date.date()-date.today()
        batch_end = "Last {} Days left".format(diff.days)
        if diff.days==0:
            batch_end = "Today Last Day"
        if date.today()>end_date.date():
            batch_end = "Batch Completed"
    else:
        batch_end = None
    return batch_end


@register.simple_tag
def remove_html_tag(string):
    cleaner = re.compile('<.*?>')
    string = re.sub(cleaner, '', string)
    return string


@register.simple_tag
def get_class_details(batch_name_string):
    batch_data = []
    b = batch_name_string.split("/")
    c = b[2].split("_")
    d = c[2]
    dt_string = d[0:4]+str('-')+d[4:6]+str('-')+d[6:8]+str(' ')+d[8:10]+str(':')+d[10:12]+str(':')+d[12:]
    dt_format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(dt_string, dt_format)

    length = c[3].split(".")[0]
    if length==int(0):
        length = "play"
    class_link = batch_name_string.replace("/", "@")
    meeting=class_link.split('@')[2].split('_')[0]

    batch_data.append(dt_object.date())
    batch_data.append(length)
    batch_data.append(class_link)
    batch_data.append(meeting)

    return batch_data



@register.simple_tag
def get_batch_ending_details(batch_date_time):
    batch_visible_status = True
    if batch_date_time:
        if batch_date_time.date() >= datetime.datetime.today().date():
            batch_visible_status = True
        else:
            batch_visible_status = False
    return batch_visible_status

@register.simple_tag
def get_batch_ending_details_student(batch_date_time):
    batch_visible_status = False
    if batch_date_time:
        if batch_date_time.date() >= datetime.datetime.today().date():
            batch_visible_status = False
        else:
            batch_visible_status = True
            batch_visible_status = "Batch Completed"
    return batch_visible_status


@register.simple_tag
def get_batch_student_dropped(batch_id,email):
    batch_obj = Batches.objects.filter(id=batch_id).first()
    for i in batch_obj.enroll_student.all():
        if i.enquiry_course_id.enquiry_id.email == email:
            enrollment_obj = Enrollments.objects.filter(id = i.id).first()
            if enrollment_obj.dropped:
                return True
            else:
                return False
    return True


@register.simple_tag
def get_upcoming_batch(text):
    # from datetime import datetime, timedelta
    # d = datetime.now().date()
    # t = timedelta((12 - d.weekday()) % 7)
    # next_weekend = (d + t).strftime('%Y-%m-%d')
    # next_weekend = datetime.strptime(next_weekend, '%Y-%m-%d')
    # next_weekend2 = next_weekend + timedelta(days=14)

    import datetime
    from datetime import timedelta
    import calendar

    next_saturday = "DD"
    next_saturday2 = "DD"
    next_monday = "DD"
    next_monday2 = "DD"

    try:
        today = datetime.date.today() #reference point. 
        next_saturday = today + datetime.timedelta((calendar.SATURDAY-today.weekday()) % 7 )
        next_saturday2 = next_saturday + timedelta(days=14)

        next_monday = today + datetime.timedelta((calendar.MONDAY-today.weekday()) % 7 )
        next_monday2 = next_monday + timedelta(days=14)


        end_next_saturday = next_saturday + +timedelta(days=45)
        end_next_saturday2 = next_saturday2 + +timedelta(days=45)
        end_next_monday = next_monday + +timedelta(days=45)
        end_next_monday2 = next_monday2 + +timedelta(days=45)
    except Exception as e:
        print(e)

    batch_list = []
    batch_list.append(next_saturday)
    batch_list.append(next_saturday2)
    batch_list.append(next_monday)
    batch_list.append(next_monday2)

    # today_date = datetime.datetime.now()
    # today_date_after = today_date+timedelta(days=90)
    batch_list.append(end_next_saturday)
    batch_list.append(end_next_saturday2)
    batch_list.append(end_next_monday)
    batch_list.append(end_next_monday2)
    # print(batch_list)
    return batch_list
 

@register.simple_tag
def get_chat_student_list(all_username):
    # print(all_username)
    # print(type(all_username))
    all_username = str(all_username)
    # print("5555555555555555555555555")
    if all_username:
        name_list = []
        all_username_list = all_username.split(",")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        # print(all_username_list)
        if all_username:
            for i in all_username_list:
                user_obj = User.objects.filter(Q(username = i.strip()) | Q(email=i.strip())).first()
                if user_obj:
                    if user_obj.first_name=="--":
                        name_list.append(i)
                    else:
                        name_list.append(user_obj.first_name)
                else:
                    name_list.append(i)  

        return name_list
    return all_username

@register.simple_tag
def get_student_name(id_list=None):
    # print(id_list)
    name_list = []
    if id_list:
        for i in id_list:
            user_name = User.objects.filter(id = i).first().first_name
            name_list.append(user_name)
    return ", ".join(name_list)



@register.simple_tag
def get_marked_link(reco_link=None):
    # print("------------------------------------------------------------------------------------------------------------------------")
    # print(reco_link)
    status = False
    if reco_link:
        reco_link = settings.BASE_URL+'/classroom/class_recording_demo/'+reco_link
        # print(reco_link)
        best_recording_obj = BestRecording.objects.filter(link=reco_link)
        if not best_recording_obj:
            reco_link = reco_link.replace("class_recording_demo","playback")
            best_recording_obj = BestRecording.objects.filter(link=reco_link)
        if best_recording_obj:
            status=True
    print(status)
    
    return status

@register.simple_tag
def get_marked_link_batch(reco_link=None):
    # print("---------------------------------------------------cc---------------------------------------------------------------------")
    # print(reco_link)
    status = False
    if reco_link:
        reco_link = settings.BASE_URL+'/classroom/class_recording_demo/'+reco_link
        # print(reco_link)
        best_recording_obj = BestRecording.objects.filter(link=reco_link)
        # print(best_recording_obj)
        if not best_recording_obj:
            # print("entring if")
            reco_link = reco_link.replace("class_recording_demo","playback")
            best_recording_obj = BestRecording.objects.filter(link=reco_link)
            # print(best_recording_obj)
        if best_recording_obj:
            status=True
    print(status)
    
    return status

@register.simple_tag
def convert_utc_to_itc(batch_date_time=None):
    print("---------------------/---------------------------------------------------------------------------------------------------")
    print(batch_date_time)
    if batch_date_time:
        from datetime import datetime, timedelta
        batch_date_time = batch_date_time+timedelta(hours=5,minutes=30)
    return batch_date_time



@register.simple_tag
def get_batch_obj_for_recording(batch_id=None,batch_type=None):
    print("---------------------/---------------------------------------------------------------------------------------------------")
    print(batch_id)
    print(batch_type)
    batch_obj = None
    if int(batch_type)==1:
        batch_obj = Batches.objects.filter(id=batch_id).first()
    elif int(batch_type) == 2:
        batch_obj = Demo.objects.filter(id=batch_id).first()
    return batch_obj


@register.simple_tag
def chek_date(end_date):
    passed=None
    if end_date:
        from datetime import date
        today_date = date.today()
        if today_date >= end_date:
            passed=True
        else:
            passed = None
    return passed


@register.simple_tag
def count_persentage(price,original_price):
    persentage=" "
    if price and original_price:
        print(persentage)
        print(original_price)
        print(price)
        persentage = int(int(price)*100/int(original_price))
        persentage = 100-persentage
        print(persentage)
    return persentage

@register.simple_tag
def get_city_sidemap_category_course(category,city):
    if city and category:
        city_specific_course = City_Specific_Course.objects.filter(course__category_name = category, city__name=city)
        # print(city_specific_course)
        return city_specific_course
    return None


@register.simple_tag
def get_link_from_message(message):
    link = "#"
    if message:
        message_part = message.split(" ")
        for i in message_part:
            if 'https' in i or 'http' in i:
                link = i
    return link


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.simple_tag
def get_category_interview_question(id):
    questions_queryset = None
    # print(id)
    if id:
        questions_queryset = InterviewQuestionTitleDescription.objects.filter(categories__id = id)
    return questions_queryset

@register.filter()
def to_int(value):
    return int(value)

@register.simple_tag
def split_time_date(string):
    if string:
        string = string.split("T")
        string = (" Time ").join(string)
        return string
    return None

@register.simple_tag
def course_review_inc_dec(review):
    if review:
        review_list = []
        review = int(review)
        review_list.append(str(('{:,}'.format(review+956))))
        review_list.append(str(('{:,}'.format(review+256))))
        review_list.append(str(('{:,}'.format(review+745))))
        return review_list
    return review


@register.simple_tag
def make_formated_number(number):
    if number:
        number = (str(('{:,}'.format(number))))
        return number
    return 0

@register.simple_tag
def get_dyna_color(test):
    import random
    clist = []
    a_list = ['#1a8cff','#9966ff','#9966ff','#99ff66','#ff1aff','#ccccff','#d98c8c','#009900','#b3b300','#0000cc','#cc3300','#0099cc','#ff9900','#00cc66']
    c1 = random.choice(a_list)
    c2 = random.choice(a_list)
    if c1==c2:
        c2 = random.choice(a_list)
    clist.append(c1)
    clist.append(c2)
    return clist

@register.simple_tag
def get_datetime_format(datetime_string):
    from datetime import datetime
    formated_datetime = 'YYYY-MM-DD'
    if datetime_string:
        formated_datetime = datetime.strptime(datetime_string,"%Y%m%d")
    return formated_datetime

@register.simple_tag
def get_batch_fee_collection_details(batch_id):
    if batch_id:
        print("*"*150)
        print(batch_id)
        batch_obj = Batches.objects.filter(id=batch_id).first()
        print(batch_obj)

        all_batch_student = batch_obj.enroll_student.all()
        total_fee = 0
        for i in all_batch_student:
            print(i.discussed_fee)
            total_fee = total_fee + int(i.discussed_fee)

    return total_fee

@register.simple_tag
def get_course_sell_option_status(course_id):
    # print(course_id)
    # print('--=-'*100)
    try:
        if course_id:
            # print('this is id'*100)
            rec_cour_obj = Recorded_Courses_name.objects.filter(course_id=course_id).last()
            if rec_cour_obj.status == True:
                # print('yes'*100)
                # print("IN IF....")
                return rec_cour_obj
            else:
                print('90'*100)
                print('this values is not true')
    # print("IN ELSE....")
    except:
        return False
@register.simple_tag
def get_gst_amount_of_fee(fee):
    fee_list = []
    if fee:
        gst_amount = round(((int(fee)*15.25428178522315)/100),2)
        after_gst = round((int(fee)-gst_amount),2)
        fee_list.append(fee)
        fee_list.append(gst_amount)
        fee_list.append(after_gst)
    return fee_list

@register.simple_tag
def get_demo_course_id(course_id):
    # print(course_id)
    # print("*"*90)
    cid=DemoSaveVideo.objects.filter(course_name_id=course_id).first()
    print(cid)
    if cid:
        return True
    else:
        return False

@register.simple_tag
def get_percent(discusfee,recive):
    if discusfee:
        # print(discusfee)
        # print("a*s"*90)
        # print(recive)
        percent=(recive/discusfee)*100
        return percent

@register.simple_tag
def replace_word(rword):
    rword = rword.replace("Course","")
    rword = rword.replace("Online","")
    rword = rword.strip()
    rword = rword+" in Other Cities"
    return rword

lead_list=[]
@register.simple_tag
def followup_response(lid):
    
    lead_list.append(lid)
    # print('anpas'*100)
    # print(lid)
    # print(lead_list)
    for z in reversed(lead_list):
        # print('this reverse',z)
        foll_obj=Followups.objects.filter(followupid_id=z)
    # print(foll_obj)
        for i in foll_obj:
            response=i.student_response
            # print(response)
            # print('lkjfd'*100)
            return response   
    
@register.simple_tag
def get_complete_recording(cid):
    # print('i m geting complete id')
    print(cid)
    com_batch=CompleteRecording.objects.filter(course_id=cid)
    if com_batch:
        return True
    else:
        return False
    


@register.simple_tag
def get_learning_path_course_count(lp_id):
    lpCourse_count = Learning_Path_Courses.objects.filter(learning_path_id = lp_id).count()
    # print("LP COUNT: ",lpCourse_count)
    return lpCourse_count


@register.simple_tag
def compare_date_for_classroom_page(batch_date):
    now = datetime.datetime.now().date()
    print(now)
    if now>=batch_date.date():
        return True
    else:
        return False



import requests
import json
@register.simple_tag
def get_couontry_from_ip(ip):
    if ip:
        try:
            endpoint = f'https://ipapi.co/{ip}/json/'
            response = requests.get(endpoint, verify = True)

            if response.status_code != 200:
                return '--'
                exit()

            data = response.json()
            print(data)
            return data['country_calling_code']
        except Exception as e:
            print(e)
            return '--'
    return '--'
