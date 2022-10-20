from pathlib import Path
import os
import django_heroku
from django.contrib.messages import constants as messages
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b&=u6_4z&(zka_7clk()myq-zzqtcw2@v2lh&c7uo-2m+=u$*j'

DEBUG = False

SITE_ID = 1

ALLOWED_HOSTS = ['https://e-shop-proj.herokuapp.com/', 'www.e-shop-proj.herokuapp.com/']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',    #add sites to installed apps
    'django.contrib.sitemaps',   #add Django sitemaps to installed apps

    # My Apps
    'user_accounts',
    'store',

    #3rd Party Apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login_required.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ecommerce_Application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce_Application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #Database Engine
        'NAME': 'dfi34pluhv7pki', #Database Name
        'USER': 'gpknyxnroztmgj', #User Name
        'PASSWORD': '9408f262124b36a2da869d48082039346ffca3ca05404aed860442cedc6d5a24', #Password
        'HOST': 'ec2-34-242-84-130.eu-west-1.compute.amazonaws.com', #Host Name (localhost)
        'PORT': '5432', #Access Port (Leave Blank)
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tags to load BootStrap class for Django message framework
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ali.alhussein.alt@gmail.com'
EMAIL_HOST_PASSWORD = 'embimgqdnklasilk'
DEFAULT_FROM_EMAIL = 'e-shop.info@eshop.com' 
APPLICATION_EMAIL = 'e-shop.info@eshop.com'

STRIPE_PUBLIC_KEY = 'pk_test_51LucX2CCcgV8lelJTaB3F6VB90LSb6UzCP2flEjOPDEhe7uWpwGYBWCIz9lwp7wRi55QOL1xdCIwhBJedHfsMy5m00Fa3HvgDW'
STRIPE_SECRET_KEY = 'sk_test_51LucX2CCcgV8lelJmrJ5Wt5UZC4VsC7rPaWaWigSXuHIJCvTLLTb6XovsOBiVCd8lSCvAIQ4PVL4iZlZbXKI8p0W00j41PpmDH'
STRIPE_WEBHOOK_SECRET = 'whsec_a53d98f400a853d4b745c17e7772d5efe714b8836eb01c35e7b064bf638909d2'

LOGIN_REQUIRED_IGNORE_PATHS = [
    r'/media/$',
    r'/media/uploads/$',
]

LOGIN_REQUIRED_IGNORE_VIEW_NAMES = [   # urls ignored by the login_required. Can be accessed with out logging in
    'home',
    'login',
    'register',
    'logout',
    'password_reset',
    'password_reset_done',
    'password_reset_confirm',
    'password_reset_complete',
    'category_products',
    'product',
    'MEDIA_URL',
]

LOGIN_REQUIRED_REDIRECT_FIELD_NAME = 'login'
LOGIN_URL = 'login'                  # sets the 'login' page as default when user tries to illegally access profile or other hidden pages
LOGOUT_REDIRECT_URL = 'login'        # sets the logout redirect to the 'login' page after logout


# MAILCHIMP CREDENTIALS
MAILCHIMP_API_KEY = 'db4e74cbae0bc972a5eb6ff3b0242274-us13'
MAILCHIMP_DATA_CENTER = 'us13'
MAILCHIMP_EMAIL_LIST_ID = '50dc17de70'