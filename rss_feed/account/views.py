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



    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user, 5)
        res = Response({'token': jwt_token})
        res.set_cookie('refresh_token', jwt_token)
        res.data = jwt_token
        return res