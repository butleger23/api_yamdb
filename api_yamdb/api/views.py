from django.contrib.auth import get_user_model, tokens
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, serializers, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserSerializer,
)
from api.viewsets import ListDestroyCreateGenreCategoryViewSet, NoPutViewSet
from api_yamdb.settings import EMAIL_HOST_USER
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CategoryViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(NoPutViewSet):
    queryset = Title.objects.all()
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(NoPutViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrModeratorOrReadOnly,
    ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_pk'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def create(self, request, *args, **kwargs):
        title = self.get_title()
        if Review.objects.filter(title=title, author=request.user).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли ревью для этой работы.'
            )
        return super().create(request, *args, **kwargs)


class CommentViewSet(NoPutViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrModeratorOrReadOnly,
    ]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_pk'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(NoPutViewSet):
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
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user, _ = User.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email'),
        )
        confirmation_code = tokens.default_token_generator.make_token(user)
        send_mail(
            subject='Yamdb confirmation code',
            message=f'Here is your confirmation code {confirmation_code}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=request.data['username'])
        if not tokens.default_token_generator.check_token(
            user, confirmation_code
        ):
            return Response(
                'Wrong confirmaton code', status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)}, status=status.HTTP_200_OK
        )
