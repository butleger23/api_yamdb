from django.shortcuts import render
from rest_framework import viewsets

from reviews.models import Category, Genres, Titles
from .viewsets import ListDeleteCreateViewSet

class CategoryViewSet(ListDeleteCreateViewSet):
    queryset = Category.objects.all()
    serializer_classes = CategorySerializer
    permission_classes = [pass,]


class GenresViewSet(ListDeleteCreateViewSet):
    queryset = Genres.objects.all()
    serializer_classes = CategorySerializer
    permission_classes = [pass,]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_classes = CategorySerializer
    permission_classes = [pass,]