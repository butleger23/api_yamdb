from random import randint
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'confirmation_code')
        read_only_fields = ('confirmation_code',)
        model = User

    def get_confirmation_code(self, obj):
        return randint(10000, 99999)

    def create(self, validated_data):
        return User.objects.create(
            confirmation_code=self.get_confirmation_code(self),
            **validated_data
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя выбрать данный username')
        return value
