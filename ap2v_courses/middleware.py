# middleware.py

from django.core.cache import cache
from .utils import (
    # custom_cache_key_courses,
    custom_cache_key_city_courses,
    # custom_cache_key_landing_page,
)
from django.urls import reverse

class CustomCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is GET and user is anonymous (not logged in)
        if request.method == 'GET' and not request.user.is_authenticated:
            # Define cache_key_func based on the URL
            # if request.path == reverse('course-listing'):
            # if request.path == reverse('all_courses'):
                # cache_key_func = custom_cache_key_courses
            # elif request.path == reverse('course-listing_city'):
            #     cache_key_func = custom_cache_key_city_courses
            if request.path == reverse('all_coursesCity'):
                cache_key_func = custom_cache_key_city_courses
            # elif request.path == reverse('landing-page'):
            #     cache_key_func = custom_cache_key_landing_page
            else:
                cache_key_func = None

            if cache_key_func:
                cache_key = cache_key_func(request)
                if cache_key:
                    cached_response = cache.get(cache_key)
                    if cached_response:
                        return cached_response

        response = self.get_response(request)

        # Cache the response for anonymous users (not logged in)
        if request.method == 'GET' and not request.user.is_authenticated:
            if cache_key_func and response.status_code == 200:
                cache.set(cache_key, response, 60 * 15)  # Cache for 15 minutes

        return response