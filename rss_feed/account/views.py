from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import views, permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views

from .serializers import UserSerializer
from .auth import JWTAuthentication
from . import jwt_tools
from .models import User

import uuid

# User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = UserSerializer


class LoginView(views.APIView):

    def post(self, request):
        user = authenticate(request=request, **request.data)
        if user:
            access_token = user.create_access_token()
            refresh_token = user.create_refresh_token()
            jwt_tools.store_in_cash(access_token)
            jwt_tools.store_in_cash(refresh_token)
            return Response(data={"Refresh token": refresh_token, "Access token":access_token}, status=status.HTTP_200_OK)
        return Response(data={"message:": "Authentication faild"}, status=status.HTTP_401_UNAUTHORIZED)


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
        return Response(data={"Refresh token": refresh_token, "Access token":access_token}, status=status.HTTP_200_OK)

