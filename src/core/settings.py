from os.path import dirname, abspath, join
from types import MappingProxyType
from typing import Tuple

from corsheaders.defaults import default_methods, default_headers
from environ import Env
from sentry_sdk import init
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from .helpers.caches import CACHES
from .helpers.default_apps import DEFAULT_APPS
from .helpers.i18n_settings import (
    DEFAULT_LOCALE_PATHS, DEFAULT_LANGUAGES
)
from .helpers.middlewares import DEFAULT_MIDDLEWARES
from .helpers.rest_framework_settings import (
    REST_FRAMEWORK_SETTINGS
)
from .helpers.storages import STORAGES, DEFAULT_STORAGE
from .helpers.templates import DEFAULT_TEMPLATES
from .helpers.validators import DEFAULT_VALIDATORS

BASE_DIR: str = dirname(dirname(abspath(__file__)))
# Environment variables
env = Env()
Env.read_env()
# Sentry
# SENTRY_DSN: str = env.str(var='SENTRY_DSN')
# integrations: Tuple = (DjangoIntegration(), CeleryIntegration())
# init(dsn=SENTRY_DSN, integrations=integrations)
#
CACHES: CACHES
# Django
DEBUG: bool = env.bool(var='DEBUG')
SECRET_KEY: str = env.str(var='SECRET_KEY')
APPEND_SLASH: bool = True
ALLOWED_HOSTS: Tuple = ('*',)
INSTALLED_APPS: Tuple = DEFAULT_APPS
MIDDLEWARE: Tuple = DEFAULT_MIDDLEWARES
ROOT_URLCONF: str = 'core.urls'
TEMPLATES: Tuple = DEFAULT_TEMPLATES
WSGI_APPLICATION: str = 'core.wsgi.application'
DATABASES: MappingProxyType = MappingProxyType({'default': env.db()})
AUTH_PASSWORD_VALIDATORS: Tuple = DEFAULT_VALIDATORS
# Security
SECURE_BROWSER_XSS_FILTER: bool = True
SESSION_COOKIE_SECURE: bool = False
X_FRAME_OPTIONS: str = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF: bool = True
CSRF_COOKIE_SECURE: bool = False
# Localization
LOCALE_PATHS: Tuple = DEFAULT_LOCALE_PATHS
LANGUAGES: Tuple = DEFAULT_LANGUAGES
LANGUAGE_CODE: str = 'en'
USE_I18N: bool = True
USE_L10N: bool = True
TIME_ZONE: str = 'Asia/Almaty'
USE_TZ: bool = True
STATIC_URL: str = '/static/'
STATIC_ROOT: str = join(BASE_DIR, 'staticfiles')
MEDIA_URL: str = '/media/'
MEDIA_ROOT: str = join(BASE_DIR, 'media')
# Corsheaders
CORS_ORIGIN_ALLOW_ALL: bool = True
CORS_ALLOW_METHODS: Tuple = default_methods
CORS_ALLOW_HEADERS: Tuple = default_headers
CORS_ALLOW_CREDENTIALS: bool = True
# Rest framework
REST_FRAMEWORK: MappingProxyType = REST_FRAMEWORK_SETTINGS
# Storage
DEFAULT_FILE_STORAGE: str = STORAGES.get(
    env.str(var='WHERE_TO_KEEP_MEDIA'), DEFAULT_STORAGE
)
# AWS S3
AWS_ACCESS_KEY_ID: str = env.str(var='AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY: str = env.str(var='AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME: str = env.str(var='AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET: bool = env.bool(var='AWS_AUTO_CREATE_BUCKET')
AWS_DEFAULT_ACL: str = env.str(var='AWS_DEFAULT_ACL')
AWS_BUCKET_ACL: str = env.str(var='AWS_BUCKET_ACL')
AWS_S3_SIGNATURE_VERSION: str = env.str(var='AWS_S3_SIGNATURE_VERSION')
AWS_S3_REGION_NAME: str = env.str(var='AWS_S3_REGION_NAME')
AWS_S3_ENCRYPTION: bool = env.bool(var='AWS_S3_ENCRYPTION')
# Celery
CELERY_BROKER_URL: str = env.str(var='CELERY_BROKER_URL')
CELERY_RESULT_BACKEND: str = env.str(var='CELERY_RESULT_BACKEND')
CELERY_TIMEZONE: str = 'Asia/Almaty'
CELERY_ENABLE_UTC: bool = True
CELERY_ACCEPT_CONTENT: Tuple = ('application/json',)
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_TASK_ACKS_LATE: bool = True
# Email
EMAIL_HOST: str = env.str(var='EMAIL_HOST')
EMAIL_PORT: int = env.int(var='EMAIL_PORT')
EMAIL_HOST_USER: str = env.str(var='EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL: str = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD: str = env.str(var='EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS: bool = env.bool(var='EMAIL_USE_TLS')
EMAIL_USE_SSL: bool = env.bool(var='EMAIL_USE_SSL')
DATE_INPUT_FORMATS = ['%d-%m-%Y']
# Debug toolbar
# if DEBUG:
#     from .helpers.debug_settings import (
#         DEFAULT_DEBUG_MIDDLEWARES, DEFAULT_DEBUG_INTERNAL_IPS,
#         DEFAULT_DEBUG_TOOLBAR_PANELS, DEFAULT_DEBUG_APPS,
#         DEFAULT_DEBUG_TOOLBAR_CONFIG
#     )
#
#     INSTALLED_APPS += ('silk',) + DEFAULT_DEBUG_APPS
#     MIDDLEWARE += tuple(
#         MIDDLEWARE[:4] + (
#             'silk.middleware.SilkyMiddleware',
#         ) + MIDDLEWARE[4:] + DEFAULT_DEBUG_MIDDLEWARES
#     )
#     SILKY_PYTHON_PROFILER = True
#     INTERNAL_IPS: Tuple = DEFAULT_DEBUG_INTERNAL_IPS
#     DEBUG_TOOLBAR_PANELS: Tuple = DEFAULT_DEBUG_TOOLBAR_PANELS
#     DEBUG_TOOLBAR_CONFIG = DEFAULT_DEBUG_TOOLBAR_CONFIG
