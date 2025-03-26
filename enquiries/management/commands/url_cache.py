from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ap2v_courses.models import Courses,City_Specific_Course
import requests
from learning_paths.models import Learning_Path,City_Specific_Learning_Path
from blogs.models import Blogs
from datetime import datetime
now = datetime.now()
from core.models import UrlCacheScriptLog

class Command(BaseCommand):
    help = 'Cacheing whole website.'

    def handle(self, *args, **kwargs):

        x = UrlCacheScriptLog(start_script = True)
        x.save()

        all_url_list = {}
        course_obj = Courses.objects.all()
        #cacheing parent course pages.....
        print("****************----------------------------------- Cacheing Course Pages----------------------------------- *********************")
        print("Total URL found : ",course_obj.count())
        for ittration,i in enumerate(course_obj):
            url = i.slug
            complete_url = "https://www.ap2v.com/"+url
            
            print("{}.) URL: {}".format(ittration+1,complete_url))
            try:
                res = requests.get(complete_url)
                all_url_list[complete_url] = str(res.status_code)+" - "+res.headers['X-Cache']
                print("Response: ",res.status_code," -------- " ,res.headers['X-Cache'])
            except Exception as e:
                print(e)
                all_url_list[complete_url] = "Error: "+str(e)

            
            # print(url)
            tags = i.tags.all()   
            print("Skils is: ", tags)
            for i in tags:
                tag_url = i.slug+"-courses"
                # print(tag_url)
                tag_complete_url = "https://www.ap2v.com/"+tag_url
                
                print("\tSkill URL is: {}\t".format(tag_complete_url))
                try:
                    res = requests.get(tag_complete_url)
                    all_url_list[tag_complete_url] = str(res.status_code)+"-"+res.headers['X-Cache']
                    print("\tSkill URL Response: ",res.status_code," -------- " ,res.headers['X-Cache'])
                except Exception as e:
                    all_url_list[tag_complete_url] = "Error: "+str(e)

            print()
        

        #cacheing child course page......
        print("**************** -----------------------------------Cacheing City Specific Course Pages----------------------------------- *********************")
        city_specific_course_obj = City_Specific_Course.objects.all()
        print("Total URL found : ",city_specific_course_obj.count())
        for j in city_specific_course_obj:
            url = j.slugs

            complete_url = "https://www.ap2v.com/"+url
            try:
                print(complete_url)
                res = requests.get(complete_url)
                all_url_list[complete_url]=str(res.status_code)+" - "+res.headers['X-Cache']
                print(res.status_code," -------- " ,res.headers['X-Cache'])
            except Exception as e:
                all_url_list[complete_url]="Error: "+str(e)
            

            complete_url1 = "https://www.ap2v.com/"+url+"/"
            print(complete_url1)
            res1 = requests.get(complete_url1)


            tags = j.course.tags.all()   
            print(tags)
            for ji in tags:
                tag_url = ji.slug+"-courses-in-{}".format(j.city.slug)
                print(tag_url)
                tag_complete_url = "https://www.ap2v.com/"+tag_url
                
                print(tag_complete_url)
                try:
                    res = requests.get(tag_complete_url)
                    all_url_list[tag_complete_url]=str(res.status_code)+" - "+res.headers['X-Cache']
                    print(res.status_code," -------- " ,res.headers['X-Cache'])
                except Exception as e:
                    all_url_list[tag_complete_url]="Error: "+str(e)

                
                
            

        #Caching Learning Path page.........
        print("*********************** ------------------------------Caching Learninf Path----------------------------------- *****************************")
        learning_path_obj = Learning_Path.objects.all()
        print("Total URL found in Learning Path : ",learning_path_obj.count())
        for k in learning_path_obj:
            url = k.slug
            complete_url = "https://www.ap2v.com/learning-path/"+url
            print(complete_url)
            try:
                res = requests.get(complete_url)
                all_url_list[complete_url] = str(res.status_code)+" - "+res.headers['X-Cache']
                print(res.status_code," -------- " ,res.headers['X-Cache'])
            except Exception as e:
                all_url_list[complete_url] = "Error: "+str(e)
            
        
        #Caching City Specific Learning Path page.........
        print("*********************** -----------------------------------Caching City Specific Learninf Path----------------------------------- *****************************")
        city_specific_learning_path_obj = City_Specific_Learning_Path.objects.all()
        print("Total URL found in City Specific Learning Path : ",city_specific_learning_path_obj.count())
        for m in city_specific_learning_path_obj:
            url = m.slug
            complete_url = "https://www.ap2v.com/learning-path/"+url
            print(complete_url)
            
            try:
                res = requests.get(complete_url)
                all_url_list[complete_url] = str(res.status_code)+" - "+res.headers['X-Cache']
                print(res.status_code," -------- " ,res.headers['X-Cache'])
            except Exception as e:
                all_url_list[complete_url] = "Error: "+str(e)

        

        #Cahching the Blogs details page.........
        print("*********************** -----------------------------------Cahching the Blogs details page------------------------------ *****************************")
        blog_obj = Blogs.objects.all()
        if blog_obj:
            for blog in blog_obj:
                url = blog.slug
                complete_url = "https://www.ap2v.com/blog/"+url
                print("Blog Complete URL: ", complete_url)
                
                try:
                    res = requests.get(complete_url)
                    all_url_list[complete_url] = str(res.status_code)+" - "+res.headers['X-Cache']
                    print(res.status_code," -------- " ,res.headers['X-Cache'])
                except Exception as e:
                    all_url_list[complete_url] = "Error: "+str(e)


    

        #Other page Cacheing...........        
        print("**************************----------------------------------- Caching Other Page -----------------------------------********************************************")     
        try:
            main_url = 'https://www.ap2v.com'
            res = requests.get(main_url)
            all_url_list[main_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(main_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[main_url]="Error: "+str(e)


        try:
            course_url = 'https://www.ap2v.com/courses/'
            res = requests.get(course_url)
            all_url_list[course_url] = (res.status_code)+" - "+res.headers['X-Cache']
            print(course_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[course_url]="Error: "+str(e)


        try:
            learning_path_url = 'https://www.ap2v.com/learning-path/'
            res = requests.get(learning_path_url)
            all_url_list[learning_path_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(learning_path_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[learning_path_url]="Error: "+str(e)


        try:
            about_us_url = 'https://www.ap2v.com/about-us/'
            res = requests.get(about_us_url)
            all_url_list[about_us_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(about_us_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[about_us_url]="Error: "+str(e)


        try:
            why_ap2v_url = 'https://www.ap2v.com/why-ap2v/'
            res = requests.get(why_ap2v_url)
            all_url_list[why_ap2v_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(why_ap2v_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[why_ap2v_url]="Error: "+str(e)


        try:
            testimonials_url = 'https://www.ap2v.com/testimonials/'
            res = requests.get(testimonials_url)
            all_url_list[testimonials_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(testimonials_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[testimonials_url]="Error: "+str(e)


        try:
            events_url = 'https://www.ap2v.com/events/'
            res = requests.get(events_url)
            all_url_list[events_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(events_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[events_url]="Error: "+str(e)


        try:
            blog_url = 'https://www.ap2v.com/blog/'
            res = requests.get(blog_url)
            all_url_list[blog_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(blog_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[blog_url]="Error: "+str(e)


        try:
            gallery_url = 'https://www.ap2v.com/gallery/'
            res = requests.get(gallery_url)
            all_url_list[gallery_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(gallery_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[gallery_url]="Error: "+str(e)


        try:
            contact_us_url = 'https://www.ap2v.com/contact-us/'
            res = requests.get(contact_us_url)
            all_url_list[contact_us_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(contact_us_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[contact_us_url]="Error: "+str(e)


        try:
            verify_url = 'https://www.ap2v.com/verify/'
            res = requests.get(verify_url)
            all_url_list[verify_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(verify_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[verify_url]="Error: "+str(e)


        try:
            refer_earnurl = 'https://www.ap2v.com/refer-earn/'
            res = requests.get(refer_earnurl)
            all_url_list[refer_earnurl]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(refer_earnurl," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[refer_earnurl]="Error: "+str(e)


        try:
            offers_url = 'https://www.ap2v.com/offers/'
            res = requests.get(offers_url)
            all_url_list[offers_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(offers_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[offers_url]="Error: "+str(e)


        try:
            sitemap_url = 'https://www.ap2v.com/sitemap/'
            res = requests.get(sitemap_url)
            all_url_list[sitemap_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(sitemap_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[sitemap_url]="Error: "+str(e)


        try:
            city_sitemap_url = 'https://www.ap2v.com/city-sitemap/'
            res = requests.get(city_sitemap_url)
            all_url_list[city_sitemap_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(city_sitemap_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[city_sitemap_url]="Error: "+str(e)


        try:
            trending_courses_url = 'https://www.ap2v.com/trending-courses/'
            res = requests.get(trending_courses_url)
            all_url_list[trending_courses_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(trending_courses_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[trending_courses_url]="Error: "+str(e)


        try:
            terms_and_conditions_url = 'https://www.ap2v.com/terms-and-conditions/'
            res = requests.get(terms_and_conditions_url)
            all_url_list[terms_and_conditions_url]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(terms_and_conditions_url," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[terms_and_conditions_url]="Error: "+str(e)


        try:
            privacy_policyurl = 'https://www.ap2v.com/privacy-policy/'
            res = requests.get(privacy_policyurl)
            all_url_list[privacy_policyurl]=str(res.status_code)+" - "+res.headers['X-Cache']
            print(privacy_policyurl," <--> ",res.status_code," -------- " ,res.headers['X-Cache'])
        except Exception as e:
            all_url_list[privacy_policyurl]="Error: "+str(e)

        


    
        print("*"*25,"END OF SCRIPT","*"*25)
        print(all_url_list)
        print("Total length of url: ",len(all_url_list))

        import csv
        # f = open('/tmp/all_url_links.csv', 'w')
        s1=now.strftime("%d_%m_%Y_%H_%M_%S")
        f = open('media/url_cache_script_log/all_url_links_{}.csv'.format(s1), 'w',newline='')
        writer = csv.writer(f)
        writer.writerow(['Sr No','Before Script Response','After Script Response','URL'])

        i = 1
        for j,m in all_url_list.items():
            try:
                res = requests.get(j)
                resp= str(res.status_code)+" - "+res.headers['X-Cache']
            except Exception as e:
                print(e)
                resp = "Error: "+str(e)
            row = (
                i,
                m,
                resp,
                j
            )
            writer.writerow(row)
            i=i+1


        UrlCacheScriptLog.objects.filter(id=x.id).update(complete_script=True,complete_on=datetime.now(),log_file='url_cache_script_log/all_url_links_{}.csv'.format(s1))