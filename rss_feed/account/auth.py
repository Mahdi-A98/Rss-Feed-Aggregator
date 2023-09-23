# In the name of GOD

from django.contrib.auth.backends import ModelBackend
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from jwt import JWT,  jwk_from_dict

jwt = JWT()
User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            jw_key = jwk_from_dict({'kty':'oct', 'k':settings.SECRET_KEY[:-1]})
            payload = jwt.decode(jwt_token, jw_key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        username_or_phone_number = payload.get('user_identifier')
        if username_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user, expiration_hours):
        # Create the JWT payload
        payload = {
            'user_identifier': user.username or user.phone or user.email,
            'exp': int((datetime.now() + timedelta(hours=expiration_hours)).timestamp()),
            # 'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'username': user.username,
            'phone_number': user.phone
        }

        # Encode the JWT with your secret key
        jw_key = jwk_from_dict({'kty':'oct', 'k':settings.SECRET_KEY[:-1]})
        jwt_token = jwt.encode(payload, jw_key, alg='HS256')
        # jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token


class UserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username=username
        password=password
        if username is None or password is None:
            return
        try:
            user= User.objects.get(Q(email=username) | Q(username=username))
            if user:
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None

        # def authenticate(self, request, username=None, password=None, **kwargs):
        #     if username is None:
        #         username = kwargs.get(UserModel.USERNAME_FIELD)
        #     if username is None or password is None:
        #         return
        #     try:
        #         user = UserModel._default_manager.get_by_natural_key(username)
        #     except UserModel.DoesNotExist:
        #         # Run the default password hasher once to reduce the timing
        #         # difference between an existing and a nonexistent user (#20760).
        #         UserModel().set_password(password)
        #     else:
        #         if user.check_password(password) and self.user_can_authenticate(user):
        #             return user



    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None