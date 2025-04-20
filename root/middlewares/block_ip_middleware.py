import logging
from django.core.cache import cache
from django.http import JsonResponse
from datetime import timedelta
from django.conf import settings

logger = logging.getLogger(__name__)

# Constants
BLOCK_TIME_SECONDS = 60 * 5     # Block for 5 minutes
MAX_FAILED_ATTEMPTS = 5         # Block after 5 failed attempts
BLOCKED_IP_KEY = "blocked_ip:{}"
FAILED_ATTEMPT_KEY = "failed_attempts:{}"


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.endpoints = settings.PROTECTED_ENDPONITS
        
    def __call__(self, request):
        if request.path in self.endpoints:
            ip = self.get_client_ip(request)

            if cache.get(BLOCKED_IP_KEY.format(ip)):
                logger.warning(f"Blocked request from IP: {ip}")
                return JsonResponse({
                    'error': 'Your IP is temporarily blocked due to too many failed login attempts.'
                }, status=403)

            response = self.get_response(request)
            return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    