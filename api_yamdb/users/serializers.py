from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .utils import get_confirmation_code
from dotenv import load_dotenv


load_dotenv()
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        read_only_fields = ('confirmation_code',)
        model = User


    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя выбрать данный username')
        return value

    def create(self, validated_data):
        confirmation_code = get_confirmation_code()
        send_mail(
            subject='Yamdb registration',
            message=f'Here is your confirmation code {confirmation_code}',
            from_email=os.getenv('host_email'),
            recipient_list=[validated_data['email']],
            fail_silently=False,
        )
        return User.objects.create(confirmation_code=confirmation_code, **validated_data)