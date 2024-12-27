import os

from django.contrib.auth import get_user_model, tokens
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin
from users.serializers import UserSerializer, TokenSerializer, SignupSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, pk=None):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user_with_provided_username = User.objects.filter(
            username=request.data['username']
        ).first()
        user_with_provided_email = User.objects.filter(
            email=request.data['email']
        ).first()
        if (
            not user_with_provided_username
            and not user_with_provided_email
        ):
            user = serializer.save()
        elif user_with_provided_username == user_with_provided_email:
            user = user_with_provided_username
        elif user_with_provided_username:
            return Response(
                'Юзер с таким username уже существует',
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif user_with_provided_email:
            return Response(
                'Юзер с таким email уже существует',
                status=status.HTTP_400_BAD_REQUEST,
            )

        confirmation_code = tokens.default_token_generator.make_token(user)
        send_mail(
            subject='Yamdb confirmation code',
            message=f'Here is your confirmation code {confirmation_code}',
            from_email=os.getenv('host_email'),
            recipient_list=[serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=request.data['username'])
        if tokens.default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)}, status=status.HTTP_200_OK
            )
        return Response(
            'Wrong confirmaton code', status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
