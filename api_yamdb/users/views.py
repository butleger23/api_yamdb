from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .utils import get_confirmation_code

from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


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
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        return ValidationError('Wrong confirmation code')

    @action(detail=False, methods=['post'])
    def signup(self, request):
        return super().create(request)
    