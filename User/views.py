from rest_framework import parsers, permissions, renderers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from User.services import *


class CreateTokenView(GenericAPIView):
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_access_token(user)
            refresh_token = generate_refresh_token()
            set_refresh_token(refresh_token=refresh_token, user=user)
            response = Response({'access_token': token, 'refresh_token': refresh_token})
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE'],
                value=token,
                expires=settings.CUSTOM_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'],
                value=refresh_token,
                expires=settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(GenericAPIView):
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'])
        new_tokens = check_and_update_refresh_token(refresh_token)
        if refresh_token and new_tokens:
            response = Response(new_tokens)
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE'],
                value=new_tokens[settings.CUSTOM_JWT['AUTH_COOKIE']],
                expires=settings.CUSTOM_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'],
                value=new_tokens[settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH']],
                expires=settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        return Response({'message': "Your token isn't valid"})
