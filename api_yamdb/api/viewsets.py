from rest_framework import mixins, viewsets
from rest_framework import generics


class ListDeleteCreateViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass
