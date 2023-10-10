# In the name of GOD

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from datetime import datetime, timedelta
from . import jwt_tools

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request, refresh_token=None):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        if access_token:
            return self.authenticat_with_token(access_token)
        if refresh_token:
            return self.authenticat_with_token(refresh_token)
        raise AuthenticationFailed("Token should be provided")
        



    def authenticat_with_token(self, jwt_token):
        prefix, jwt_token = jwt_token.split()  # clean the token
        if prefix != settings.JWT_CONF.get("token_prefix"): 
            raise AuthenticationFailed("Token prefix doesn't match")

        payload, error = jwt_tools.decode_jwt_token(jwt_token)
        if payload is None:
            raise error
        user_id = payload.get('user_identifier')
        if user_id is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        if not jwt_tools.verify_exp(payload): 
            raise AuthenticationFailed("Token expired")
        
        if not user_id == jwt_tools.verify_jti(payload):
            raise AuthenticationFailed("Invalid user")

        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        return user, payload


class UserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username=username
        password=password
        if username is None or password is None:
            raise AuthenticationFailed("You should provide credentials !!")
        try:
            user= User.objects.get(Q(email=username) | Q(username=username))
            if user:
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
