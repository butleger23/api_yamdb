from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from .viewsets import ListDeleteCreateViewSet
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsAdminOrReadOnly
from .filters import TitleFilter


class CategoryViewSet(ListDeleteCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly,]


class GenreViewSet(ListDeleteCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly,]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
