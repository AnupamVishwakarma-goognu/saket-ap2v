
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-7lqmpt#k4p+k3d+^bf0u3!omc@bd+tyij61+8abcf1x%9#7na6'
DEBUG = True
ALLOWED_HOSTS = ['anquira.ap2v.com', 'www.ap2v.com','127.0.0.1']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "compressor",
    'communication',
    'social_django',
    'bluejeans',
    'batches',
    'courses',
    'enquiries',
    'enrolls',
    'instructors',
    'users',
    'website',
    'followups',
    'django_filters',
    'pure_pagination',
    'promotions',
    'activity',
    'demo',
    'reporting',
    'ap2v_courses',
    'blogs',
    'classroom',
    'events',
    'gallery',
    'home',
    'landing_page',
    'learning_paths',
    'seo',
    'testimonials',
    'taggit',
    'location_field.apps.DefaultConfig',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.humanize',
    'chats',
    'django_chatter',
    'sitemap_generate',
    'django.contrib.sitemaps',
    'core',
    'payment',
    'feedback',
    'recording_sessions',
    'ap2v_e_store',
]

CKEDITOR_UPLOAD_PATH = "uploads/"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
)

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'anquira_v2.virtualhostmiddleware.VirtualHostMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'anquira_v2.ap2v_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.breadcrumb',
                'home.context_processors.common_divisions',
                'home.context_processors.city_block',
                'home.context_processors.seo',
                'home.context_processors.skills',
                'home.context_processors.side_bar_testimonials',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'anquira_v2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1013330998823-5ucnm08cu6fhqlhog5vonrn8if9q5fob.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'o3gYzCzFOZ2etBuFlCsU1rIs'

LOGIN_REDIRECT_URL = '/'

# custom model
AUTH_USER_MODEL = 'users.CustomUserModel'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css':[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js':[
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
#STATIC_ROOT = ''
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ABS_URL = "https://www.ap2v.com/media/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4,
    'MARGIN_PAGES_DISPLAYED': 3,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "ranasaket19110@gmail.com"
EMAIL_HOST_PASSWORD = "qyft oliq yeiz canu"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'file2': {
            'format': '%(asctime)s %(message)s'
        },
        'file3': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            # 'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug_anquira.log'
        },
        'file2': {
            # 'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file2',
            'filename': '/tmp/enquiry_log.log'
        },
        'file3': {
            # 'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file3',
            'filename': '/tmp/junk_enquiry.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        "second_log": {
            'handlers': ['file2'],
            'level': 'DEBUG'
        },
        "junk_enq_log": {
            'handlers': ['file3'],
            'level': 'INFO'
        }
    }
}


SMS_URL="https://goognu.com/?mobile={mobile}&body={body}"
API_KEY="CONNTOANQUIRA@3685"

NO_COURSE_ID = 139

LIVE_CONFIGRATION_ID = 1
TAGGIT_CASE_INSENSITIVE = False

CHATTER_BASE_TEMPLATE = "classroom/chat_base.html"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            },
        },
}

ASGI_APPLICATION = 'anquira_v2.routing.application'

# sitemaps settings
SITEMAP_MAPPING = 'anquira_v2.ap2v_urls.sitemaps'
SITEMAP_INDEX_NAME = 'sitemap-index'
SITEMAPS_VIEW_NAME = 'django.contrib.sitemaps.views.sitemap'
SITEMAP_MEDIA_PATH = 'sitemaps'
SITEMAP_HOST = 'www.ap2v.com'
SITEMAP_PROTO = 'https'
SITEMAP_PORT = '443'


BLUEJEANS_USERNAME = "neerajkumar1248.nk@gmail.com"
BLUEJEANS_PASSWORD = "Neeraj@123"
MODERATOR_PASSCODE = 8253
BLUEJEANS_COMPANY = "AP2V"
BLUEJEANS_TITLE = "Instructor"

FAST2SMS_AUTHORIZATION_KEY = 'wTiOROSJyQ8ho0nxX777stW1eCu96goxLboLeMNgUZtJFeeiPsaQdQZ7CYMc'
FAST2SMS_SENDER_ID = 'TXTIND'

# BASE_URL="https://www.ap2v.com"
BASE_URL="http://127.0.0.1:8001"

BITLY_ACCESS_TOKEN = "fe4d18da594a83d9a2a733f7924605b636b20d64"
BITLY_GUID = "Bl84eOEAWSY"

DEFAULT_INSTRUCTOR_EMAIL = "ranasaket19110@gmail.com"

REPORT_SENT_TO_EMAILS = ['saket@goognu.com']

ADMIN_EMAIL = ''

COUNSELOR_LIST = [25,26]
REGISTERED_BY= 795
TEMP_RECORDING_STORE = '/opt'
ACCESS_KEY = ''
AWS_SECRET_KEY = ''
BUCKETNAME = ''

CITY_COURSES_META_TITLE = "<Course Name> Course in <City> - AP2V"
CITY_COURSES_META_DESCRIPTION = "Get <Course Name> Certification & Training in <City> - Check Upcoming Batches, Watch Live Class Video, View Top Companies Hiring AP2V Students"
CITY_COURSES_META_KEYWORDS = "<Course> Training in <City>, <Course> Institute in <City> ,<Course> Training Institute in <City>, <Course> Training Centre in <City>, <Course> Centre in <City>, <Course> Course in <City>, <Course> Coaching in <City>, <Course> Classes in <City>, <Course> Certification in <City>, <Course> Certification Course in <City>, <Course> Certification Cost in <City>, Best <Course> Institute in <City>, <Course> Course Duration & Fees in <City>"

RAZORPAY_KEY = ""
RAZORPAY_SECERT = ""

# APPEND_SLASH = False

FEEDBACK_EMAIL_NOTIFICATION = ['saket@goognu.com']

ZOOM_API_KEY = ""
ZOOM_API_SECRET = ""
ZOOM_ADMIN_EMAIL = ""

GOOGLE_FACKEBOOK_TAG = False

ENROLLMENT_FEE_GST_RATE = 18

DEFAULT_FILE_STORAGES = "/tmp/"

HIRINGGO_LINK = ""

try:
    from .local_settings import *
    from .local_settings2 import *
except ImportError as e:
    pass

SESSION_COOKIE_SECURE = True

REASSIGN_NOTIFICATION_EMAILS = ['saket@goognu.com']

SMS_CHAR_LIMIT = 200

CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESILT_SERIALIZER = "json"
CELRRY_TASK_SERIALIZER="json"

SHOW_COURSE_COURSEL = 1


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': 1100,
        'height':500,
    },
}


