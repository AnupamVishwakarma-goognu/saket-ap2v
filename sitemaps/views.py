from django.contrib.sitemaps import Sitemap
from ap2v_courses.models import Courses, City_Specific_Course, City
from learning_paths.models import Learning_Path, City_Specific_Learning_Path
from home.models import Category
from django.urls import reverse
from datetime import date
from taggit.models import Tag

class CourseSitemap(Sitemap):
    name = 'course'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        # return Courses.objects.order_by('id')
        return Courses.objects.order_by('id').filter(active_inactive=True)

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/{}".format(item.slug)

class CityCourseSitemap(Sitemap):
    name = 'city-course'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return City_Specific_Course.objects.order_by('id').filter(active_inactive=True)

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/{}".format(item.slugs)

class LearningPathSitemap(Sitemap):
    name = 'learning-path'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Learning_Path.objects.order_by('id')

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/learning-path/{}".format(item.slug)

class CityLearningPathSitemap(Sitemap):
    name = 'city-learning-path'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return City_Specific_Learning_Path.objects.order_by('id')

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/learning-path/{}".format(item.slug)


class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    name = "static-pages"
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['contact-us', 'about-us', 'privacy-policy', 'terms-and-conditions', 'city-sitemap', 'refer_and_earn', 'gallery', 'course-listing', 'events', 'blogs']

    def location(self, item):
        return reverse(item)

class CityTagSitemap(Sitemap):
    name = 'city-skill'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        items_list = []
        for tag in Tag.objects.order_by('id'):
            if tag.taggit_taggeditem_items.count() > 0:
                for city_obj in City.objects.all():
                    tag_courses = City_Specific_Course.objects.filter(course__tags__slug__in=[tag],city__slug=city_obj.slug)
                    if len(tag_courses) >= 1:
                        skill_slug = "{}-courses-in-{}".format(tag.slug,city_obj.slug)
                        items_list.append(skill_slug)
        return items_list

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/{}".format(item)

class TagSitemap(Sitemap):
    name = 'skill'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        items_list = []

        for tag in Tag.objects.order_by('id'):
            tag_courses = Courses.objects.filter(tags__slug__in=[tag])

            if len(tag_courses) >= 1:
                skill_slug = "{}".format(tag.slug,)
                items_list.append(skill_slug)

        return items_list

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/{}-courses".format(item)


class CategorySitemap(Sitemap):
    name = 'category'
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Category.objects.order_by('id')

    def lastmod(self, item):
        return date.today()

    def location(self, item):
        return "/category/{}".format(item.slug)

