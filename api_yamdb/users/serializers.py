from random import randint
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirmation_code = (
        serializers.SerializerMethodField()
    )  # Скорее всего придется убрать когда буду делать подтверждение по email

    class Meta:
        fields = ('username', 'email', 'confirmation_code')
        model = User

    def get_confirmation_code(self, obj):
        return randint(10000, 99999)
