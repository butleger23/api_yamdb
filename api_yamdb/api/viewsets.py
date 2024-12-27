from rest_framework import mixins, viewsets, generics


class ListDeleteCreateViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass
