from types import MappingProxyType

PAGINATION_CLASS: str = 'rest_framework.pagination.LimitOffsetPagination'

REST_FRAMEWORK_SETTINGS: MappingProxyType = MappingProxyType({
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ), 'DEFAULT_FILTER_BACKENDS': (),
    'DATETIME_FORMAT': "%d/%m/%Y %H:%M:%S",
    'DEFAULT_PAGINATION_CLASS': PAGINATION_CLASS, 'PAGE_SIZE': 8
})
