from typing import Tuple

DEFAULT_APPS: Tuple = (
    # django apps
    'django.contrib.admin', 'django.contrib.staticfiles',
    'django.contrib.contenttypes', 'django.contrib.auth',
    'django.contrib.messages', 'django.contrib.sessions',
    # side apps
    'corsheaders', 'rest_framework',
    'drf_yasg', 'django_extensions',
    # project apps
    'core.flight',
)
