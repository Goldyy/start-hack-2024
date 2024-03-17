import os
from pathlib import Path
from dotenv import load_dotenv
from celery.schedules import solar
from datetime import timedelta
from .logging import addLoggingLevel
import logging

load_dotenv()

LOG_DIR = os.getenv("LOG_DIR", "/usr/src/app/shared-data/logs/backend.log")
LOG_LEVEL = os.getenv("API_LOG_LEVEL", "INFO")
addLoggingLevel('TRACE', logging.DEBUG - 5)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)

#ensure that the log directory exists
log_dir = os.path.dirname(LOG_DIR)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def get_log_style():
    if LOG_LEVEL == "DEBUG":
        return "verbose"
    else:
        return "simple"


def get_secret(key, default):
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read()
    return value

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },   
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "filename": "/usr/src/app/shared-data/logs/backend.log",
            "formatter": "verbose",
        },
        "null": {
            "class": "logging.NullHandler",
        },    
    },
    "loggers": {
        "": {
            "handlers": ["console","file"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.server": {
            "handlers": ["null"],
            "level": LOG_LEVEL,
            "propagate": False
        },
        "django.request": {
            "handlers": ["console","file"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["null"],
            "level": LOG_LEVEL,
            "propagate": True
        },
    },
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_secret("API_SECRET_KEY", "")

DEBUG = (os.environ.get('API_DEBUG_MODE', default=False) == 'True')

# fetch allowed hosts from environment variable
ALLOWED_HOSTS = os.getenv("API_ALLOWED_HOSTS", "").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("API_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("API_ALLOWED_ORIGINS", "").split(",")

# Application definition
INSTALLED_APPS = [
    # django things
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    
    # admin
    # "django.contrib.admin",
    
    # prometheus
    "django_prometheus",
    
    # ovo-hunters custom apps
    "apps.ovohunters_auth",
    "apps.ovohunters_starthack",
    
    # swagger
    "drf_spectacular",
    "drf_spectacular_sidecar",
    'oauth2_provider',
]


MIDDLEWARE = [   
    "api.middlewares.RequestLoggingMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    'django.middleware.security.SecurityMiddleware',    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # 'apps.ovohunters_auth.middlewares.KeycloakAuthorizationMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    
]

ROOT_URLCONF = "api.urls"

SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@5.10.0", # default
    "TITLE": "OVO-Hunters Awesome App",
    "DESCRIPTION": "OVO-Hunters Awesome App",
    "VERSION": "1.0.0",
    'OAUTH2_FLOWS': ['implicit'],
    'OAUTH2_AUTHORIZATION_URL': 'http://127.0.0.1:9080/realms/tars/protocol/openid-connect/auth',   
    'OAUTH2_SCOPES': None,
    'USE_SESSION_AUTH': True,
    'SWAGGER_UI_SETTINGS': {
        #'oauth2RedirectUrl': 'http://127.0.0.1:9081/static/drf_spectacular_sidecar/swagger-ui-dist/oauth2-redirect.html',
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "api.wsgi.application"
testing_mode = os.getenv("DJANGO_TESTING", "False") == "True"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": os.getenv("API_DATABASE_NAME"),
        "USER": os.getenv("API_DATABASE_USERNAME"),
        "PASSWORD": get_secret("API_DATABASE_PASSWORD", ""),
        "HOST": os.getenv("API_DATABASE_HOST"),
        "PORT": os.getenv("API_DATABASE_PORT"),
    }
}
    

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TZ", "UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.getenv("API_STATIC_URL", "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "api/static/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# AUTH_USER_MODEL = 'fnc_auth.LoginProfile'

# security reasons
SECURE_HSTS_SECONDS = 31536000
# Without this, your site cannot be submitted to the browser preload list.
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# @todo: is available via http now
SECURE_SSL_REDIRECT = False
# Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
SESSION_COOKIE_SECURE = True
#  Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
CSRF_COOKIE_SECURE = True
