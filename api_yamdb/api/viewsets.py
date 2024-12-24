from rest_framework import mixins
from rest_framework import generics


class ListDeleteCreateViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, generics.GenericAPIView
):
    pass
