from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import views, permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views

from .serializers import UserSerializer
from .auth import JWTAuthentication
from . import jwt_tools
from .models import User
from rss_feed.publisher import Publisher

import uuid
import json

publisher = Publisher()


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = UserSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # my code
        publisher.publish(message="user registered successfully", queue='signup-login')
        return response


class LoginView(views.APIView):

    def post(self, request):
        user = authenticate(request=request, **request.data)
        if user:
            access_token = user.create_access_token()
            refresh_token = user.create_refresh_token()
            jwt_tools.store_in_cash(access_token)
            jwt_tools.store_in_cash(refresh_token)
            publisher.publish(message=f"{user.username} logged in successfully", queue='signup-login')
            return Response(data={"Refresh token": refresh_token, "Access token":access_token}, status=status.HTTP_200_OK)
        publisher.error_publish(message=f"user with ({json.dumps(request.data)}) cridential faild to login", queue='signup-login')
        return Response(data={"message:": str(_("Authentication faild"))}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(views.APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        auth = JWTAuthentication()
        user, payload = auth.authenticat_with_token(refresh_token)
        jwt_tools.delete_jti_from_cache(payload['jti'])
        jti = uuid.uuid4().hex
        access_token = user.create_access_token(jti)
        refresh_token = user.create_refresh_token(jti)
        jwt_tools.store_in_cash(access_token)
        publisher.publish(message=f"{user.username} got refresh token", queue='signup-login')
        return Response(data={"Refresh token": refresh_token, "Access token":access_token}, status=status.HTTP_200_OK)

class ProfileView(views.APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class LogoutView(views.APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        _, refresh_token = request.data.get("refresh_token").split()
        _, access_token = request.META.get("HTTP_AUTHORIZATION").split()
        access_token_payload, ac_error = jwt_tools.decode_jwt_token(access_token)
        refresh_token_payload, ref_error = jwt_tools.decode_jwt_token(refresh_token)
        if not (access_token_payload.get("user_identifier") == refresh_token_payload.get("user_identifier") == request.user.id):
            publisher.publish(message=f"{request.user.username} faild to to logout cause of diffrent AT uid:{access_token_payload.get('user_identifier')} and RT uid:{refresh_token_payload.get('user_identifier')}", queue='signup-login')
            return Response(data={"message": str(_("invalid user id"))}, status=status.HTTP_400_BAD_REQUEST)
        jwt_tools.delete_jti_from_cache(access_token_payload.get("jti"))
        jwt_tools.delete_jti_from_cache(refresh_token_payload.get("jti"))
        publisher.publish(message=f"{request.user.username} logged out", queue='signup-login')
        return Response(data={"message": str(_("Logout successfully"))}, status=status.HTTP_200_OK)
        
