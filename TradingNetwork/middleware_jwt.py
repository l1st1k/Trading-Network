import traceback

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._force_auth_user = self.get_jwt_user(request)

    @staticmethod
    def get_jwt_user(request):
        user_jwt = get_user(request)
        if user_jwt.is_authenticated:
            return user_jwt
        token = request.COOKIES.get(settings.CUSTOM_JWT['AUTH_COOKIE'], None)
        user_jwt = AnonymousUser()
        if token:
            try:
                user_jwt = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
                user_jwt = User.objects.get(
                    username=user_jwt['username']
                )

            except (ObjectDoesNotExist, jwt.exceptions.ExpiredSignatureError):
                traceback.print_exc()
        return user_jwt
