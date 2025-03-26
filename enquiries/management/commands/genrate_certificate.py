from django.core.management.base import BaseCommand
from batches.models import Batches,StudentCertificateIssued
from django.conf import settings
import os
import csv
import datetime
from django.utils import timezone as tz
from users.models import CertificateId,CustomUserModel
from communication.views import send_certificate_email
from enrolls.models import Enrollments

class Command(BaseCommand):
    help = 'Genrate Certificate When Batch Complete'

    def handle(self, *args, **kwargs):
        #batch_obj = Batches.objects.filter(certificate_issued=False,end_date_time__lte = tz.now())
        batch_obj = Batches.objects.filter(certificate_issued=False,end_date_time__lte = tz.now(),batch_type="1")
        print(batch_obj)

        for i in batch_obj:
            course_list = []
            for m in i.courses.all():
                course_list.append(m.name)

            for j in i.enroll_student.all():
                if not j.dropped and j.enroll_type=='1':
                    name = j.enquiry_course_id.enquiry_id.full_name
                    course = " and ".join(course_list)

                    print("Name : ",j.enquiry_course_id.enquiry_id.full_name)
                    print("Course : "," and ".join(course_list))

                    email = j.enquiry_course_id.enquiry_id.email
                    user_obj = CustomUserModel.objects.filter(email = email).first()
                    if user_obj:
                        user_cert_id_obj = CertificateId.objects.filter(user = user_obj.id).first()
                        if not user_cert_id_obj:
                            x = CertificateId(
                                user_id = user_obj.id
                            )
                            x.save()
                            # print("Certificate id Genrate of : ", x.cert_id)
                        user_cert_id_obj = CertificateId.objects.filter(user = user_obj.id).first()

                        u_id = user_obj.id
                    else:
                        create_user = CustomUserModel(
                            first_name = name,
                            email = email.lower(),
                            username = email.replace("@","."),
                            is_verified = False,
                            user_type = "student"
                        )
                        create_user.save()

                        user_cert_id_obj = CertificateId.objects.filter(user = create_user.id).first()
                        if not user_cert_id_obj:
                            x = CertificateId(
                                user_id = create_user.id
                            )
                            x.save()
                            # print("Certificate id Genrate of : ", x.cert_id)
                        user_cert_id_obj = CertificateId.objects.filter(user = create_user.id).first()

                        u_id = create_user.id

                    if not StudentCertificateIssued.objects.filter(user_id=u_id,batch_id=i.id,enroll_id=j.id).exists():
                        y = StudentCertificateIssued(
                            name = name,
                            course = course,
                            date = i.end_date_time,
                            code = user_cert_id_obj.cert_id,
                            user_id = u_id,
                            batch_id = i.id,
                            enroll_id = j.id
                        )
                        y.save()
                        # print(y.id)
                        # print(y.uuid)

                        enroll_obj = Enrollments.objects.filter(id = j.id).first()
                        if enroll_obj:
                            Enrollments.objects.filter(id = j.id).update(
                                certificate_issued = True,
                                certificate_uuid = y.uuid
                            )
                        link = str(settings.BASE_URL)+"/classroom/certificate/"+str(y.uuid)
                        print(link)
                        # print("Sending Mail....")
                        send_certificate_email(name,link,email,course)
                    else:
                        print("Already Genrated...")

            Batches.objects.filter(id = i.id).update(
                certificate_issued = True
            )

            print("-----------")

        
