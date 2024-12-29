from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, permissions

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorOrModeratorOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from api.viewsets import ListDestroyCreateGenreCategoryViewSet, NoPutViewSet
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(NoPutViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly,]
    # permission_classes = [permissions.AllowAny,]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        genre_slugs = self.request.data.get('genre', [])
        genres = Genre.objects.filter(slug__in=genre_slugs)
        serializer.save(genre=genres)

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        if 'category' in validated_data:
            category_slug = validated_data.pop('category')
            category = Category.objects.get(slug=category_slug)
            instance = serializer.instance
            instance.category = category
        
        if 'genre' in validated_data:
            genre_slugs = validated_data.pop('genre')
            genres = Genre.objects.filter(slug__in=genre_slugs)
            instance.genre.set(genres)
        
        serializer.save()


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
