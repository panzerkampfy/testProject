from asyncio import exceptions
from datetime import datetime

from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'first_name', 'last_name', 'date_joined']

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    city = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_joined = serializers.DateTimeField(default=datetime.now)

    def validate_username(self, username):
        uniqueness = User.objects.filter(username=username).exists()
        if username and uniqueness:
            raise serializers.ValidationError(
                "A user is already registered with this username.")
        return username

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(UserDetailsSerializer):
    city = serializers.CharField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('city',)


class CustomLoginSerializer(LoginSerializer):
    def _validate_username_email(self, username, email, password):
        user = None
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = 'Must include either "username" or "email" and "password".'
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_orm(self, username, email, password):
        if username:
            return self._validate_username_email(username, '', password)

        return None

    def get_auth_user_using_allauth(self, username, email, password):
        pass

    def validate_auth_user_status(self, user):
        pass
