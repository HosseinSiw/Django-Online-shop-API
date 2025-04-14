from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.conf import settings


class AutoAuthForDevMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.DEBUG and settings.DEV_AUTH:
            User = get_user_model()
            try:
                user = User.objects.get(email='h1@admin.com')
                request.user = user
            except user.DoesNotExist:
                pass
            