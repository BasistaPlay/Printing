"""
Django settings for ecomerce project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v1fiaup#2ni$7o)+u(uzkc9n$((#nrayt9__52wtm#651%-tpj'
RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}
RECAPTCHA_REQUIRED_SCORE = 0.85

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['ericprint.com', 'www.ericprint.com']

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['https://ericprint.com', 'https://www.ericprint.com']

DEBUG = False



# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django_recaptcha',
    'rosetta',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'colorfield',
    'django.contrib.staticfiles',
    'ckeditor',
    "phonenumber_field",
    'ckeditor_uploader',
    'User_app',
    'home',
    'design',
    'product_details',
    'Product',
    'shoping_cart',
    'payments',
    'honeypot',
    'compressor',
    'webpack_loader',
    #'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
]

ROOT_URLCONF = 'ecomerce.urls'

TEMPLATES = [
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'shoping_cart.context_processor.cart_total_amount',
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.i18n',
        ],
    },
},
]

WSGI_APPLICATION = 'ecomerce.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ericprint',
        'USER': 'ericprint',
        'PASSWORD': 'ericprint',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = abspath(os.path.dirname(__file__))

MEDIA_ROOT = abspath(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'User_app.user'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'lv-lv'

TIME_ZONE = 'Europe/Riga'

USE_I18N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('lv', gettext('Latvian')),
    ('en', gettext('English')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'lv'
MODELTRANSLATION_LANGUAGES = ('lv', 'en')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'  # URL ceļš, kuru izmantos, lai piekļūtu statiskajiem failiem

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "language_chooser": True
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mafiagameeee@gmail.com'
EMAIL_HOST_PASSWORD = 'hjmyxkzttzahgfib'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'mafiagameeee@gmail.com'

ROSETTA_REQUIRES_AUTH = False


CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'height': 300,
        'width': 600,
    'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['NumberedList','BulletedList'],
            ['Indent','Outdent'],
            ['Maximize'],
            ['Styles', 'Format', 'Font', 'FontSize'],
        ]
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Design",
    "site_header": "Design",
    "welcome_sign": "Welcome",
    "show_sidebar": True,
    "language_chooser": True,
    "language": "lv",
    "navigation_expanded": True,
    "hide_apps": ["'sites'"],
    "show_ui_builder": False,
    "related_modal_active": False,
    "topmenu_links": [],
    "usermenu_links": [],
    "theme": "home",
    "icons": {
        "app.Model": "fas fa-tachometer-alt",
        "auth.User": "fas fa-user",
        "Product.Product": "fas fa-box",
        "home.CustomDesign": "fas fa-palette",
        "User_app.ContactMessage": "fas fa-envelope",
        "User_app.Contact": "fas fa-address-book",
        "User_app.user": "fas fa-user",
        "home.Price": "fas fa-dollar-sign",
        "home.Product_list": "fas fa-list",
        "product_details.Color": "fas fa-paint-brush",
        "product_details.Size": "fas fa-ruler",
        "design.designs": "fas fa-tshirt",
        "Product.category": "fas fa-tags",
        "home.Purchase": "fas fa-receipt",
        "django_recaptcha.RecaptchaKeys": "fas fa-shield-alt",

        "Payments.BankDetails": "fas fa-university",
        "Payments.Purchase": "fas fa-shopping-cart",
        "Payments.GiftCode": "fas fa-gift",
        "User_App.FAQ": "fas fa-question-circle"
    },
}

CART_SESSION_ID = 'cart'

SOCIALACCOUNT_LOGIN_ON_GET = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'

FILE_CHARSET = 'utf-8'


SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_ADAPTER = 'User_app.adapters.MySocialAccountAdapter'

# Recaptcha settings
RECAPTCHA_PUBLIC_KEY = '6LfuiuQpAAAAAEq03FdKts-9bZ6KIcF9T8K7w4KY'
RECAPTCHA_PRIVATE_KEY = '6LfuiuQpAAAAAGFFXYQQ4vaPzyJVuT9tpUJK3THe'

# Stripe settings
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET')

HONEYPOT_FIELD_NAME = 'email2'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

try:
    from ecomerce.local_settings import *
except ImportError:
    pass