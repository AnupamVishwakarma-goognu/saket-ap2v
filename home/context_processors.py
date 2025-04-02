from blogs.models import Blogs,InterviewQuestionTitleDescription
from courses.models import *
from home.models import SidebarCategory
from home.models import Configrations
from testimonials.models import *
from taggit.models import Tag
from django.conf import settings
import random
from seo.models import *
from django.core.exceptions import ObjectDoesNotExist
from learning_paths.models import Learning_Path, City_Specific_Learning_Path
from ap2v_courses.models import Courses, Category, City_Specific_Course, City
from django.urls import reverse
from testimonials.models import Text
from seo.models import Meta, SkillsContent
from urllib.parse import urljoin
import os.path
from communication.views import get_number 
from core.models import OfferEndDate,AuthToken
import geoip2.database

def get_tag_class(count):					# to give darker background to tag with more tagged items
	if count < 2:
		return 'tag1'
	elif count >= 2 and count <= 4:
		return 'tag2'
	elif count > 4 and count <= 6:
		return 'tag3'
	elif count > 6 and count <= 8:
		return 'tag4'
	else :
		return 'tag5'

# def auto_rand_number(request):
# 	try:
# 		phone_number = get_number(request)
# 	except:
# 		phone_number = '+91 8306996216'
# 	return {"number": phone_number}

def city_block(request):
    ctx = {'city_block': []}

    match_url_names = ['learning-path-listing','learning-path-detail','course-listing','course-detail']


    # return if blank
    if not request.resolver_match:
        return ctx

    url_name = request.resolver_match.url_name

    if url_name not in match_url_names:
        return ctx

    if url_name == 'course-detail':
        slug = request.resolver_match.kwargs.get('slug')
        try:
            course = Courses.objects.get(slug=slug,active_inactive=True)
        except:
            course = City_Specific_Course.objects.filter(slugs=slug,active_inactive=True).first()
            if course:
                course = course.course
        
        if course:
            for course in City_Specific_Course.objects.filter(course=course,active_inactive=True):
                tmp_d = {}
                tmp_d['name'] = course.city.name
                tmp_d['href'] = (reverse('course-detail', args=[course.slugs])).rstrip('/')
                tmp_d['cname'] = course.name

                ctx['city_block'].append(tmp_d)
                print(ctx['city_block'])
                print("888888888888")

    elif url_name == 'learning-path-detail':
        slug = request.resolver_match.kwargs.get('slug')
        try:
            lp = Learning_Path.objects.get(slug=slug)
        except:
            lp = City_Specific_Learning_Path.objects.get(slug=slug).parent_learning_path

        for lp in City_Specific_Learning_Path.objects.filter(parent_learning_path=lp):
            tmp_d = {}
            tmp_d['name'] = lp.city.name
            tmp_d['href'] = (reverse('learning-path-detail', args=[lp.slug])).rstrip('/')

            ctx['city_block'].append(tmp_d)

    return ctx


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def common_divisions(request):
    ctx = {}
    ctx['learning_paths'] = Learning_Path.objects.all()
    ctx['trending_courses'] = Courses.objects.filter(trending=True,active_inactive=True)
    ctx['trending_course_footer'] = Courses.objects.filter(trending=True,active_inactive=True)
    ctx['category_all'] = Category.objects.all()
    ctx['category_search_show'] = Category.objects.all()[:4]
    ctx['trending_learning_path'] = Learning_Path.objects.filter(trending=True)
    ctx['learning_path_footer'] = Learning_Path.objects.filter(trending=True)
    ctx['all_course'] = Courses.objects.filter(active_inactive=True)
    ctx['feature_course'] = Courses.objects.filter(featured=True,active_inactive=True)
    ctx['snownumber']=list(range(0, 201))

    ctx['tranding_course_in_other_city'] = City_Specific_Course.objects.filter(show_tranding_in_footer=True, active_inactive=True)
    ctx['tranding_learning_path_in_other_city'] = City_Specific_Learning_Path.objects.filter(show_tranding_in_footer=True)

    avilable_course_city = City_Specific_Course.objects.all().values_list('city',flat=True).distinct()
    city_obj_q = City.objects.filter(id__in = avilable_course_city)
    ctx['city_obj_q']=city_obj_q

    avilable_learning_paths = City_Specific_Course.objects.all().values_list('city',flat=True).distinct()
    city_obj_q_lp = City.objects.filter(id__in = avilable_learning_paths)
    ctx['city_obj_q_lp']=city_obj_q_lp
    tag_code = settings.GOOGLE_FACKEBOOK_TAG
    ctx['tag_code'] = tag_code
    import uuid
    ctx['rand_uuid'] = str(uuid.uuid4())
    ip = get_client_ip(request)
    try:
        reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')
        response = reader.country(ip)
        ip_country = "in"
        reader.close()

    except Exception as e:
        print(e)
        ip_country = "in"  
    
    ctx['mylip'] = ip_country
    print("IP country:",ctx['mylip'])
    ctx['hiringoo_link'] = settings.HIRINGGO_LINK

    return ctx


def breadcrumb(request):
    # default Home
    d = {'breadcrumb': [{'name': 'Home', 'path': '/'},]}
    base_uri_org = request.path
    base_uri = None
    if request.path != "/":
        base_uri = request.path.rstrip("/")

    # return blank if None
    if not request.resolver_match:
        return {}

    url_name = request.resolver_match.url_name


    static_pages = ["contact-us", "about-us", "privacy-policy", "terms-and-conditions", "city-sitemap", "sitemap", "refer_and_earn", "gallery", "all_events", "blogs", "trending-courses", "featured-courses", "course-listing", "learning-path-listing", "offers"]

    dynamic_pages = {
            "blogs_display": ["blogs",],
            "course-detail": ["course-listing",],
            "display_category": []
        }
    
    dynamic_pages_learning_path = {
            "learning-path-detail": ["learning-path-listing",],
        }

    dynamic_pages_model_mapping = {
            "blogs_display": [{'model': Blogs, 'slug_field': Blogs.slug},],
            "course-detail": [{'model': Courses, 'slug_field': Courses.slug}, {'model': City_Specific_Course, 'slug_field': City_Specific_Course.slugs}],

            }
    
    dynamic_pages_model_mapping_learnig_path = {
            "learning-path-detail": [{'model': Learning_Path, 'slug_field': Learning_Path.slug}, {'model': City_Specific_Learning_Path, 'slug_field': City_Specific_Learning_Path.slug}]
            }

    city_course = ['course-listing_city']
    city_learning_path_list = ['city-learning-paths']
    if url_name in city_course:
        name = request.path.strip("/").title()
        name = name.replace("-"," ")
        path = "/"+request.path.strip("/")
        d['breadcrumb'].append({'name': name, 'path': path})


    elif url_name in static_pages:
        uri_meta = Meta.objects.filter(uri=base_uri)
        if uri_meta.exists():
            b = {'name': uri_meta.breadcrumb, 'path': base_uri_org}
            d['breadcrumb'].append(b)
    elif url_name in dynamic_pages:
        slug = os.path.basename(base_uri)

        for b in dynamic_pages[url_name]:
            url_path_org = reverse(b)
            url_path = url_path_org.rstrip("/")
            m_obj = Meta.objects.filter(uri=url_path)
            if m_obj.exists():
                m_obj = m_obj.first()
                try:
                    Courses.objects.get(slug = slug)
                    d['breadcrumb'].append({'name': m_obj.breadcrumb, 'path': url_path_org})
                except Exception as e:
                    print(e)

        if url_name in dynamic_pages_model_mapping:

            for e in dynamic_pages_model_mapping[url_name]: 
                try:
                    try:
                        obj = e['model'].objects.get(slugs=slug)
                        name = "Courses in " + obj.city.name
                        path = "/courses-in-"+obj.city.slug
                        d['breadcrumb'].append({'name': name, 'path': path})
                    except:
                        obj = e['model'].objects.get(slug=slug)

                    breadcrumb_text = obj.breadcrumb
                    d['breadcrumb'].append({'name': breadcrumb_text, 'path': base_uri_org})
                except:
                    pass
                else:
                    break
    
    elif url_name in dynamic_pages_learning_path:
        slug = os.path.basename(base_uri)
        for b in dynamic_pages_learning_path[url_name]:
            url_path_org = reverse(b)
            url_path = url_path_org.rstrip("/")
            m_obj = Meta.objects.filter(uri=url_path)
            if m_obj.exists():
                try:
                    Learning_Path.objects.get(slug = slug)
                    d['breadcrumb'].append({'name': m_obj.breadcrumb, 'path': url_path_org})
                except Exception as e:
                    print(e)

        if url_name in dynamic_pages_model_mapping_learnig_path:

            for e in dynamic_pages_model_mapping_learnig_path[url_name]: 
                try:
                    try:
                        obj = e['model'].objects.get(slug=slug)
                        # print(obj)
                        x= obj.city.name
                        uri_meta = Meta.objects.get(uri="/learning-path")
                        b = {'name': uri_meta.breadcrumb, 'path': '/learning-path/'}
                        d['breadcrumb'].append(b)

                        name = "Learning Paths in "+obj.city.name
                        path = "/learning-paths-in-"+obj.city.slug
                        d['breadcrumb'].append({'name': name, 'path': path})
                    except:
                        obj = e['model'].objects.get(slug=slug)

                    breadcrumb_text = obj.breadcrumb
                    d['breadcrumb'].append({'name': breadcrumb_text, 'path': base_uri_org})
                except:
                    pass
                else:
                    break

    elif url_name=="city_sitemap_category":
        base_uri_city = (base_uri.split("/"))[-1]
        d['breadcrumb'].append({'name': "city site map", 'path': "/city-sitemap/"})
        d['breadcrumb'].append({'name': "tranning "+base_uri_city, 'path': base_uri})

    elif url_name in city_learning_path_list:

        uri_meta = Meta.objects.get(uri="/learning-path")
        b = {'name': uri_meta.breadcrumb, 'path': '/learning-path/'}
        d['breadcrumb'].append(b)

        name = request.path.strip("/").title()
        name = name.replace("-"," ")
        path = "/"+request.path.strip("/")
        d['breadcrumb'].append({'name': name, 'path': path})
    

    return d


def seo(request):
    d = {'seo': {}}
    base_uri = request.path

    if request.path != "/":
        base_uri = request.path.rstrip("/")
   
    # return blank if None
    if not request.resolver_match:
        return d
    
    url_name = request.resolver_match.url_name
    

    try:
        slug = base_uri.split("/")[-1]

        if url_name == "course-detail":
            try:
                uri_meta = Courses.objects.get(slug=slug)
                d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.photo.url)
            except Courses.DoesNotExist:
                uri_meta = City_Specific_Course.objects.get(slugs=slug)
                d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.course.photo.url)
                d['seo']['geo_placename'] = uri_meta.city.geo_placename
                d['seo']['geo_region'] = uri_meta.city.geo_region
                d['seo']['geo_position'] = uri_meta.city.geo_position
                d['seo']['geo_icbm'] = uri_meta.city.geo_icbm

        elif url_name == "learning-path-detail":
            try:
                uri_meta = Learning_Path.objects.get(slug=slug)
                d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.banner_image.url)
        
            except Learning_Path.DoesNotExist:
                uri_meta = City_Specific_Learning_Path.objects.get(slug=slug)
                d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.parent_learning_path.banner_image.url)

                # geo meta
                d['seo']['geo_placename'] = uri_meta.city.geo_placename
                d['seo']['geo_region'] = uri_meta.city.geo_region
                d['seo']['geo_position'] = uri_meta.city.geo_position
                d['seo']['geo_icbm'] = uri_meta.city.geo_icbm
                
        elif url_name == 'display_tag':
            tag_slug = slug.rstrip("courses").rstrip("-")
            tag_name = Tag.objects.get(slug=tag_slug).name
            tagged_courses_count = Courses.objects.filter(tags__slug__in=[tag_slug]).count()
            d['seo']['title'] = "{tag_name} Courses : {tag_name} Training & Certification".format(tag_name=tag_name)
            d['seo']['head'] = "{tag_name} Courses".format(tag_name=tag_name)
            d['seo']['description'] = "Best {tagged_count}+ {tag_name} Courses at AP2V.com - Check {tag_name} Learning Path, Trending Courses in {tag_name} with Certification. Most Popular {tag_name} Course for Beginners".format(tag_name=tag_name, tagged_count=tagged_courses_count)

            # breadcrumb
            breadcrumb_title = slug.replace("-"," ").title()
            d['breadcrumb'] = [{'name': 'Home', 'path': '/'}, {'name': breadcrumb_title, 'path': '/{}'.format(slug)}]

            return d

        elif url_name == 'display_city_tag':
            tag_slug, city_slug = slug.split("-in-")
            tag_slug = tag_slug.rstrip("courses").rstrip("-")
            city_obj = City.objects.get(slug=city_slug)

            tag_name = Tag.objects.get(slug=tag_slug).name
            tagged_courses_count = City_Specific_Course.objects.filter(course__tags__slug__in=[tag_slug],city__slug=city_slug).count()
            d['seo']['title'] = "{tag_name} Courses in {city} : {tag_name} Training & Certification".format(tag_name=tag_name, city=city_obj.name)
            d['seo']['head'] = "{tag_name} Courses in {city}".format(tag_name=tag_name, city=city_obj.name)
            d['seo']['description'] = "Best {count}+ {tag_name} Courses in {city} - Check {tag_name} Learning Path, Trending Courses in {tag_name} with Certification. Most Popular {tag_name} Course for Beginners".format(tag_name=tag_name, city=city_obj.name, count=tagged_courses_count)

            d['seo']['geo_placename'] = city_obj.geo_placename
            d['seo']['geo_region'] = city_obj.geo_region
            d['seo']['geo_position'] = city_obj.geo_position
            d['seo']['geo_icbm'] = city_obj.geo_icbm

            # breadcrumb
            breadcrumb_title = slug.replace("-"," ").title()
            d['breadcrumb'] = [{'name': 'Home', 'path': '/'}, {'name': breadcrumb_title, 'path': '/{}'.format(slug)}]

            return d

        elif url_name == "display_category":
            category_obj = Category.objects.get(slug=slug)
            courses_count = Courses.objects.filter(category_name = category_obj).count()
            d['seo']['title'] = "{category_name} Courses : Training | Certification & Fundamentals".format(category_name=category_obj.name)
            d['seo']['head'] = "{category_name} Courses".format(category_name=category_obj.name)
            d['seo']['description'] = "Best {count}+ {category_name} Courses at AP2V.com - Check {category_name} Learning Path, Trending Courses in {category_name} with Certification. Most Popular {category_name} Course for Beginners.".format(category_name=category_obj.name, count=courses_count)

            # breadcrumb
            breadcrumb_title = slug.replace("-"," ").title()
            d['breadcrumb'] = [{'name': 'Home', 'path': '/'}, {'name': breadcrumb_title, 'path': '/{}'.format(slug)}]

            return d

        elif url_name == "display_city_category":
            category_slug, city_slug = slug.split("-in-")
            city_obj = City.objects.get(slug=city_slug)
            category_obj = Category.objects.get(slug=category_slug)
            courses_count = City_Specific_Course.objects.filter(course__category_name=category_obj, city__slug=city_slug).count()
            d['seo']['title'] = "{category_name} Courses in {city}: Training | Certification & Fundamentals".format(category_name=category_obj.name, city=city_obj.name)
            d['seo']['head'] = "{category_name} Courses in {city}".format(category_name=category_obj.name, city=city_obj.name)
            d['seo']['description'] = "Best {count}+ {category_name} Courses in {city} - Check {category_name} Learning Path, Trending Courses in {category_name} with Certification. Most Popular {category_name} Course for Beginners.".format(category_name=category_obj.name, city=city_obj.name, count=courses_count)
            d['seo']['geo_placename'] = city_obj.geo_placename
            d['seo']['geo_region'] = city_obj.geo_region
            d['seo']['geo_position'] = city_obj.geo_position
            d['seo']['geo_icbm'] = city_obj.geo_icbm
            breadcrumb_title = slug.replace("-"," ").title()
            d['breadcrumb'] = [{'name': 'Home', 'path': '/'}, {'name': breadcrumb_title, 'path': '/{}'.format(slug)}]

            return d

        elif url_name == "blogs_display":
            uri_meta = Blogs.objects.get(slug=slug)
            
            d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.image.url)
        elif url_name == "interview_questions_display":
            uri_meta = InterviewQuestionTitleDescription.objects.get(slug=slug)
            d['seo']['image'] = urljoin(settings.MEDIA_ABS_URL,uri_meta.image.url)
            
        else:
            uri_meta = Meta.objects.get(uri=base_uri)
    except Exception as e:
        if url_name == "city_sitemap_category":
            uri_meta={}
            city = base_uri.split("/")[-1]
            d['seo']['title'] = "IT Training in {} | City Site Map ".format(city)
            return d
        elif url_name =="course-listing_city":
            uri_meta={}
            city = base_uri.split("-")[-1]
            d['seo']['title'] = "IT Training Online in {city} | Online IT Training Courses".format(city=city)
            return d
        elif url_name =="city-learning-paths":
            uri_meta={}
            city = base_uri.split("-")[-1]
            d['seo']['title'] = "IT Courses Online in {city} | IT Professional Training Center {city}".format(city=city)
            return d

        return {}

    d['seo']['title'] = uri_meta.title
    d['seo']['description'] = uri_meta.meta_description
    d['seo']['keywords'] = uri_meta.meta_keyword
    d['seo']['gplus_headers'] = uri_meta.gplus_headers
    d['seo']['twitter_headers'] = uri_meta.twitter_headers
    d['seo']['fb_og_headers'] = uri_meta.fb_og_headers
    print(d)


    return d

def side_bar_testimonials(request):
	testimonials=Text.objects.all().order_by('-date')[:5]
	return {'side_bar_testimonials':testimonials}


def skills(request):
    d = {'skill': {}}
    base_uri = request.path

    if request.path != "/":
        base_uri = request.path.rstrip("/")
   
    # return blank if None
    if not request.resolver_match:
        return d
    
    url_name = request.resolver_match.url_name
    

    try:
        slug = base_uri.split("/")[-1]
        skill_obj = SkillsContent.objects.get(uri=base_uri)
        d['skill']['heading'] = skill_obj.heading
        d['skill']['disc'] = skill_obj.discription
            
    except Exception as e:
        print(e)
    print('***'*100)
    print('d'*100)
    print(d)
    return d