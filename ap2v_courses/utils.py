# utils.py

from django.core.cache import cache
from django.urls import reverse
from django.utils.cache import get_cache_key

# def custom_cache_key_courses(request, *args, **kwargs):
#     if request.user.is_authenticated:
#         return None  # Return None to bypass caching for authenticated users
#     prefix = 'courses'
#     url = reverse('course-listing', args=args, kwargs=kwargs)
#     # url = reverse('all_courses', args=args, kwargs=kwargs)
#     cache_key = get_cache_key(request, key_prefix=prefix, version=1)
#     return f"{cache_key}:{url}"

def custom_cache_key_city_courses(request, *args, **kwargs):
    if request.user.is_authenticated:
        return None  # Return None to bypass caching for authenticated users
    prefix = 'city_courses'
    url = reverse('all_coursesCity', args=args, kwargs=kwargs)
    cache_key = get_cache_key(request, key_prefix=prefix, version=1)
    return f"{cache_key}:{url}"

# def custom_cache_key_landing_page(request, *args, **kwargs):
#     if request.user.is_authenticated:
#         return None  # Return None to bypass caching for authenticated users
#     prefix = 'landing_page'
#     url = reverse('landing-page', args=args, kwargs=kwargs)
#     cache_key = get_cache_key(request, key_prefix=prefix, version=1)
#     return f"{cache_key}:{url}"
