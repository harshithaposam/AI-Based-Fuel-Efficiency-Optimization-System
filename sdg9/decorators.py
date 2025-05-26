import functools
import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger('sdg9')

def handle_api_errors(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f'API Error in {f.__name__}: {str(e)}', exc_info=True)
            return JsonResponse({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }, status=500)
    return wrapper

def handle_view_errors(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f'View Error in {f.__name__}: {str(e)}', exc_info=True)
            return render(args[0], 'sdg9/error.html', {
                'error_message': str(e)
            }, status=500)
    return wrapper