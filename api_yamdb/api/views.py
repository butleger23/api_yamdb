from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review
from .viewsets import ListDeleteCreateViewSet
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrModeratorOrReadOnly
from .filters import TitleFilter


class Crud5ViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']


class CategoryViewSet(ListDeleteCreateViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListDeleteCreateViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(Crud5ViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly,]

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


class CommentViewSet(Crud5ViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly,]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_pk'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
