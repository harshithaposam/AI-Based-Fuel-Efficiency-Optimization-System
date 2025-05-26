import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger('sdg9')

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f'Error processing request: {exception}', exc_info=True)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'An unexpected error occurred',
                'details': str(exception)
            }, status=500)

        return render(request, 'sdg9/error.html', {
            'error_message': str(exception)
        }, status=500)