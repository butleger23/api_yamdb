from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import UserRegistrationSerializer


User = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer