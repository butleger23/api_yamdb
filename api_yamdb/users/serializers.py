import re

from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from rest_framework import serializers


load_dotenv()
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя выбрать данный username')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[])
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_username(self, value):
        USERNAME_REGEXP = re.compile(r'^[\w.@+-]+\Z')
        if value == 'me' or not re.fullmatch(USERNAME_REGEXP, value):
            raise serializers.ValidationError('Нельзя выбрать данный username')
        return value
