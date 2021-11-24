from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from dj_rest_auth.app_settings import create_token
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.serializers import TokenSerializer, JWTSerializerWithExpiration, JWTSerializer
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView as login
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):

            if getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = JWTSerializer

        else:
            response_serializer = TokenSerializer
        return response_serializer

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.user = User.objects.get(username=serializer.data.get('username'))
        if getattr(settings, 'REST_USE_JWT', False):
            self.access_token, self.refresh_token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)
        data = login.get_response(self).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def verify(self, request):
        try:
            user = User.objects.get(is_verified=False)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.is_verified = True
        user.save()

        return Response(status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/"


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/"


class VkLogin(SocialLoginView):
    adapter_class = VKOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/"


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/"
