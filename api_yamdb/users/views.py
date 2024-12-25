from random import randint
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_confirmation_code(self):
        return str(randint(10000, 99999))

    def perform_create(self, serializer):
        serializer.save(confirmation_code=self.get_confirmation_code())


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def token(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            raise ValidationError('Bad request')
        if confirmation_code == user.confirmation_code:
            return Response({'token': 'abra'}) # сделать на jwt
        return Response('Wrong confirmation code')

    @action(detail=False, methods=['post'])
    def signup(self, request):
        return super().create(request)

    def get_confirmation_code(self):
        return str(randint(10000, 99999))

    def perform_create(self, serializer):
        serializer.save(confirmation_code=self.get_confirmation_code())