from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.conf import settings


class AutoAuthForDevMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.DEBUG and settings.DEV_AUTH:
            User = get_user_model()
            
            try:
                user, _ = User.objects.get_or_create(email='admin@admin.com', password='123/asd',
                                                     is_active=True,
                                                     is_superuser=True)
                request.user = user
            except user.DoesNotExist:
                pass
