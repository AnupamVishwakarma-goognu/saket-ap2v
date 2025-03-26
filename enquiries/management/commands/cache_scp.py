from django.core.management.base import BaseCommand
from urllib.request import urlopen
from time import time
from django.conf import settings
from django.core.mail import send_mail
import smtplib
import sys
import requests 


class Command(BaseCommand):
    help = 'Correct Space Issue in content and other text data'
    def handle(self, *args, **kwargs): 
        URLS=['https://www.ap2v.com/aws-training-faridabad', 'https://www.ap2v.com/','https://www.ap2v.com/aws-training-kochi','https://www.ap2v.com/python-training-ahmedabad','https://www.ap2v.com/python-training-kochi','https://www.ap2v.com/kubernetes-cka-training-kochi','https://www.ap2v.com/aws-training-in-chandigarh','https://www.ap2v.com/aws-training-in-gurgaon','https://www.ap2v.com/gcp-training-kochi','https://www.ap2v.com/gcp-training-in-pune','https://www.ap2v.com/kubernetes-training-in-ameerpet','https://www.ap2v.com/microsoft-azure-training-kochi','https://www.ap2v.com/devops-online-training-course','https://www.ap2v.com/rhcsa-certification-training-online','https://www.ap2v.com/django-course-training-online',]
        
        gmail_user = "apvenquiry@gmail.com"
        gmail_password = "wulzwcwnhctfoqjx"
        
        for url in URLS:
            # website = urlopen(url)
            # open_time = time()
            # output = website.read()
            # close_time = time()
            # website.close()
            # taking_time=round(close_time-open_time,3)
            # print('The loading time of website is',round(close_time-open_time,3),'seconds')
            response = requests.get(url) 
            taking_time=round(response.elapsed.total_seconds(),3)
            # print response 
            # print(response) 
            
            # print elapsed time 
            print(taking_time)
            print(url)
            if taking_time>0.500:
    
                sent_from = gmail_user
                to = ['ashu@goognu.com','arun.yadav@goognu.com', 'aashish@goognu.com','neeraj@goognu.com','neerajkumar1248.nk@gmail.com']
                # to = ['aashish@goognu.com','aashishchhachhiya@gmail.com']
                subject = 'Alert: URL Response taking time..'

                print('this page is slow ', url)
                body='Dear Sir/Madam\n,Loading of pages taking time {} MS.\nStandard loading of pages taking time 500 MS \nKindly run the Cache script.\n URL: {}.'.format(taking_time,url)
                # send_mail('Cache Clearing Script not run', MASSAGE, "settings.EMAIL_HOST_USER", [settings.REPORT_SENT_TO_EMAILS])

                # email_text = """\
                #     From: %s
                #     To: %s
                #     Subject: %s

                #     %s
                #     """ % (sent_from, ", ".join(to), subject, body)

                try:
                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtp_server.ehlo()
                    smtp_server.login(gmail_user, gmail_password)
                    # smtp_server.sendmail("apvenquiry@gmail.com", ['aashish@goognu.com'], body)
                    send_mail(subject, body, sent_from, to)
                    smtp_server.close()
                    print ("Email sent successfully!")
                except Exception as ex:
                    print ("Something went wrong….",ex)
                
                break

