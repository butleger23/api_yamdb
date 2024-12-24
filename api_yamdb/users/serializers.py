from random import randint
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # confirmation_code = serializers.CharField(max_length=5)

    class Meta:
        fields = ('username', 'email', 'confirmation_code')
        read_only_fields = ('confirmation_code',)
        model = User


    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя выбрать данный username')
        return value
