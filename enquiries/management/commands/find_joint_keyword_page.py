from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ap2v_courses.models import Courses,City_Specific_Course
import requests
from learning_paths.models import Learning_Path,City_Specific_Learning_Path
from bs4 import BeautifulSoup
import urllib.request
import re
import csv
from django.http import HttpResponse, JsonResponse
import os

class Command(BaseCommand):
    help = 'Cacheing whole website.'

    def handle(self, *args, **kwargs):
        # #Joint Page Learning Path page.........
        # print("*********************** ------------------------------Joint Page Learninf Path----------------------------------- *****************************")
        # learning_path_obj = Learning_Path.objects.all()
        # # print("Total URL found in Learning Path : ",learning_path_obj.count())
        # no = 1
        # for k in learning_path_obj:
        #     if no ==1:
        #         url = k.slug
        #         complete_url = "https://www.ap2v.com/learning-path/"+url
        #         print(complete_url)
        #         res = requests.get(complete_url)
        #         # print(res.status_code," -------- " ,res.headers['X-Cache'])

        #         fp = urllib.request.urlopen("https://www.ap2v.com/learning-path/python-developer")
        #         mybytes = fp.read()
        #         mystr = mybytes.decode("utf8")
        #         fp.close()
        #         # print(mystr)
        #         soup = BeautifulSoup(mystr)
        #         divTag = soup.find_all("div", {"class": "banner-inner--left-pan d-flex flex-column justify-content-center"})
        #         print("------------------------------------------------------------Main Content--------------------------------------------------------------------------------------------")
        #         print(divTag[0].get_text())
        #         print("------------------------------------------------------------End Main Content--------------------------------------------------------------------------------------------")


        #         no=no+1

        #         re_obj = re.search('(\w\<strong|strong\>\w)', str(soup))

        #         if re_obj:
        #             print(re_obj.group(0))

        # --------------------------------------------------------------------------------------------------

        #f = open('D:/find_joint_keyword_page.csv', 'w')
        f = open('/tmp/find_joint_keyword_page.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['Type','id','url'])

        course_obj = Courses.objects.all()
        print("****************----------------------------------- Joint Keyword Course Pages----------------------------------- *********************")
        print("Total URL found : ",course_obj.count())
        for i in course_obj:
            url = i.slug
            complete_url = "https://www.ap2v.com/"+url
            print(complete_url)

            fp = urllib.request.urlopen(complete_url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr)
            # divTag = soup.find_all("div", {"class": "banner-inner--left-pan d-flex flex-column justify-content-center"})

            re_obj = re.search('(\w\<strong|strong\>\w)', str(soup))

            if re_obj:
                print(re_obj.group(0))
                row = (
                    'Course-Parent',
                    i.id,
                    i.slug,
                )
                writer.writerow(row)
        


        print("**************** -----------------------------------Joint Keyword City Specific Course Pages----------------------------------- *********************")
        city_specific_course_obj = City_Specific_Course.objects.all()
        print("Total URL found : ",city_specific_course_obj.count())
        for j in city_specific_course_obj:
            url = j.slugs
            complete_url = "https://www.ap2v.com/"+url
            print(complete_url)

            fp = urllib.request.urlopen(complete_url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr)
            # divTag = soup.find_all("div", {"class": "banner-inner--left-pan d-flex flex-column justify-content-center"})

            re_obj = re.search('(\w\<strong|strong\>\w)', str(soup))

            if re_obj:
                print(re_obj.group(0))
                row = (
                    'City-Specific-Child',
                    j.id,
                    j.slugs,
                )
                writer.writerow(row)



        print("*********************** ------------------------------Joint Keyword Learninf Path----------------------------------- *****************************")
        learning_path_obj = Learning_Path.objects.all()
        print("Total URL found in Learning Path : ",learning_path_obj.count())
        for k in learning_path_obj:
            url = k.slug
            complete_url = "https://www.ap2v.com/learning-path/"+url
            print(complete_url)

            fp = urllib.request.urlopen(complete_url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr)
            # divTag = soup.find_all("div", {"class": "banner-inner--left-pan d-flex flex-column justify-content-center"})

            re_obj = re.search('(\w\<strong|strong\>\w)', str(soup))

            if re_obj:
                print(re_obj.group(0))
                row = (
                    'Learning-Path-Parent',
                    k.id,
                    k.slug,
                )
                writer.writerow(row)
        


        print("*********************** -----------------------------------Joint Keyword City Specific Learninf Path----------------------------------- *****************************")
        city_specific_learning_path_obj = City_Specific_Learning_Path.objects.all()
        print("Total URL found in City Specific Learning Path : ",city_specific_learning_path_obj.count())
        for m in city_specific_learning_path_obj:
            url = m.slug
            complete_url = "https://www.ap2v.com/learning-path/"+url
            print(complete_url)

            fp = urllib.request.urlopen(complete_url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            soup = BeautifulSoup(mystr)
            # divTag = soup.find_all("div", {"class": "banner-inner--left-pan d-flex flex-column justify-content-center"})

            re_obj = re.search('(\w\<strong|strong\>\w)', str(soup))

            if re_obj:
                print(re_obj.group(0))
                row = (
                    'City-Specific-Learning-Path-Child',
                    m.id,
                    m.slug,
                )
                writer.writerow(row)
        
        f.close()
