from datetime import datetime

from dj_rest_auth.app_settings import create_token
from dj_rest_auth.utils import jwt_encode
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import User
from .serializers import RegisterSerializer, CustomLoginSerializer
from dj_rest_auth.models import TokenModel
from dj_rest_auth.views import LoginView as login
from dj_rest_auth.serializers import TokenSerializer, JWTSerializerWithExpiration, JWTSerializer


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
