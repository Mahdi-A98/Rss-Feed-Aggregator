from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class META:
        model = User
        fields = ['username', 'phone', 'first_name', 'last_name', 'password']

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()