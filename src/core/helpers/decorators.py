from copy import deepcopy
from functools import wraps

from rest_framework.response import Response
from rest_framework.status import is_success

from . import codes


def response_wrapper():
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            if is_success(response.status_code) and isinstance(response, Response):
                data = deepcopy(response.data)
                response.data = {'results': data, 'code': codes.OK}
            else:
                return response
            return response

        return inner

    return decorator
