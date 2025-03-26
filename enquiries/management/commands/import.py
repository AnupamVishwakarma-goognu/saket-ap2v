from django.core.management.base import BaseCommand
from enquiries.models import (
    Followups, Enquiries, EnquiryCourses
)
from courses.models import Courses
from datetime import datetime
from users.models import CustomUserModel
import csv

course_data = {
    "Amazon Web Services": {"value": 5, "name": "Amazon Web Services"},
    "Red Hat Certified Engineer": {"value": 2, "name": "Red Hat Certified Engineer"},
    "Artificial Intelligence": {"value": 21, "name": "Artificial Intelligence"},
    "Automation with Ansible": {"value": 16, "name": "Automation with Ansible"},
    "Bash shell": {"value": 22, "name": "Bash shell"},
    "Python-Basics": {"value": 4, "name": "Python-Basics"},
    "CL310 - openstack rhce": {"value": 15, "name": "CL310 - openstack rhce"},
    "Courses": {"value": 23, "name": "Courses"},
    "Devops - I": {"value": 8, "name": "Devops - I"},
    "Devops Foundation": {"value": 24, "name": "Devops Foundation"},
    "Kubernetes": {"value": 12, "name": "Kubernetes"},
    "Dot-Net": {"value": 25, "name": "Dot-Net"},
    "Redhat Virtualization": {"value": 26, "name": "Redhat Virtualization"},
    "Exam": {"value": 27, "name": ['EX200', 'EX210', "EX407"]},
    "Java-Core": {"value": 28, "name": "Java-Core"},
    "Jenkins": {"value": 8, "name": "Jenkins"},
    "Openstack - CL210": {"value": 15, "name": "Openstack - CL210"},
    "Puppet-Admin-I": {"value": 29, "name": "Puppet-Admin-I"},
    "opensthift Admin": {"value": 14, "name": "opensthift Admin"},
    "Python Advance": {"value": 30, "name": "Python Advance"},
    "Red Hat Certified System Administrator": {"value": 1, "name": "Red Hat Certified System Administrator"},
    "W3Python": {"value": 31, "name": "W3Python"}
}

location_data = {
    "AP2V Solutions": {"value": "Gurgaon", "name": "AP2V Solutions"},
    "AP2V Solutions Noida": {"value": "Noida", "name": "AP2V Solutions Noida"}
}

interest_level = {
    "Desperate to Join (Super Hot)": {"value": 1},
    "Highly Interested (Very Hot)": {"value": 2},
    "May Be Interested (Warm)": {"value": 3},
    "Interested (Hot)": {"value": 4},
    "Interested but Hesitant/Confused (Lukewarm)": {"value": 5},
    "Interest Level": {"value": 6}
}

assigned_by = {
    "Ashutosh Taiwal": {"value": 1, "name": "Ashutosh Taiwal"},
    "Assigned To": {"value": 2, "name": "Assigned To"},
    "Kirti": {"value": 3, "name": "Kirti"},
    "Manjeet": {"value": 4, "name": "Manjeet"},
    "megha": {"value": 5, "name": "megha"},
    "neha": {"value": 6, "name": "neha"},
    "Noida AP2V": {"value": 7, "name": "Noida AP2V"},
    "Pooja Kumari": {"value": 8, "name": "Pooja Kumari"},
    "Priya Saini": {"value": 9, "name": "Priya Saini"},
    "Priyanka": {"value": 10, "name": "Priyanka"},
    "Richa": {"value": 11, "name": "Richa"},
    "Vishal Saini": {"value": 12, "name": "Vishal Saini"}
}


class Command(BaseCommand):
    help = "import excel data in enquiry & followups"

    def add_arguments(self, parser):
        parser.add_argument('-e', '--enquiry', type=str, help="Enquiry Excel sheet", required=False)
        parser.add_argument('-f', '--followup', type=str, help="Followup Excel sheet", required=False)

    def handle(self, *args, **options):
        enquiry_file = options.get('enquiry')
        followup_file = options.get('followup')
        
        if not enquiry_file and not followup_file:
            print("File not provided")
            return
        with open(enquiry_file, 'r') as f:
            r = csv.reader(f)
            counter =0
            for row in r:
                try:
                    counter += 1
                    if counter < 4:
                        continue
                    print(counter)
                    
                    if counter == 10:
                        # break
                        pass

                    d={}
                    try:
                        d['date'] = datetime.strptime(row[0], '%m/%d/%Y %H:%M')
                    except:
                        d['date'] = datetime.strptime(row[0], '%d-%b-%y')
                    d['name'] = "{} {}".format(row[1],row[2])
                    d['email'] = row[3]
                    d['mobile'] = row[4]
                    d['course'] = row[7]
                    d['branch'] = row[12]
                    d['source_type'] = row[8]
                    # d['interest_leve']=row[9]
                    d['next_followup'] = datetime.strptime("{} {}".format(row[9],row[10]), '%m/%d/%Y %H:%M:%S') if row[9] else ''
                    d['followup_comment'] = row[11]
                    d['assigned_to']=row[13]
                    # print('*'*20)
                    # print(d)
                    # print(row)
                    # print('#'*20)
                    self.create_enquiry(d)
                except Exception as e:
                    print("#"*20,"EXCEPTION","#"*20)                
                    print(e)
                    print(row)
                    print("#"*20,"EXCEPTION","#"*20,'\n'*5)                

    def create_enquiry(self,data):
        '''
            reference = models.CharField(max_length=250, choices=ReferenceModeChoices.choice, null= True)
            email = models.EmailField()
            alternative_email = models.EmailField(null=True, blank=True)
            full_name = models.CharField(max_length=255)
            mobile = models.CharField(max_length=300)
            alternative_mobile = models.CharField(max_length=300, null=True, blank=True)
            company_name = models.CharField(max_length=300)
            designation = models.CharField(max_length=300)
            courses = models.ManyToManyField(Courses, blank=True)
            batch_days = models.CharField(max_length=255)
            enquiry_level = models.PositiveSmallIntegerField(default=1, choices=EnquiryLevelChoices.choice)
            discard = models.BooleanField(default=False, null=True, blank=True)
            training_mode = models.PositiveSmallIntegerField(default=1, choices=TrainingModeChoices.choice)
            batch_time = models.CharField(max_length=255, default=True)
            branch_location = models.CharField(max_length=300, choices = BRANCH_LOCATION, null= True)
            # assigned_by = models.PositiveIntegerField(default=9, null=True, blank=True, choices=AssignedByChoices.choice)
            assigned_by = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
            interested_batch = models.BooleanField(default=False)
            added_on = models.DateTimeField(auto_now_add=True)
        '''

        enq,created=Enquiries.objects.get_or_create(email = data.get('email'),mobile = data.get('mobile'))
        enq.reference = data.get('source')
        enq.full_name=data.get('name')
        enq.branch_location=data.get('branch')
        enq.added_on=data.get('date')
        enq.save()

        course,created =Courses.objects.get_or_create(name=data.get('course'),defaults={'duration':0,'price':0,'url':''})
        EnquiryCourses.objects.get_or_create(enquiry_id=enq,courses=course)
        user =None
        if data.get('assigned_to'):
            user,created =CustomUserModel.objects.get_or_create(first_name=data.get('assigned_to'),username=data.get('assigned_to'))
            enq.assigned_by=user
            enq.save()


        '''
            followupid = models.ForeignKey(Enquiries, on_delete=models.PROTECT,null=True)
            # enquiry_courses = models.ForeignKey(EnquiryCourses, on_delete=models.PROTECT)
            followup_mode = models.CharField(max_length=300, choices=TYPES_OF_FOLLOWUPS_MODE)
            response = models.CharField(max_length=300, choices=TYPES_OF_FOLLOWUPS)
            next_followup = models.DateTimeField(null = True)
            comments = models.TextField()
            status = models.BooleanField(default=False, null=True, blank=True)
            discard = models.BooleanField(
            default=False,
            null=True,
            blank=True
            )
            assigned_user = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True)
            added_on = models.DateTimeField( auto_now_add=True)
        '''
        fl,created = Followups.objects.get_or_create(followupid=enq)
        # fl.response=data.get('comment')
        fl.comments = data.get('followup_comment')
        if data.get('next_followup'):
            fl.next_followup = data.get('next_followup')
        else:
            fl.discard=True
        if user:
            fl.assigned_user=user
        fl.save()