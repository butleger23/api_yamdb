from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListDestroyCreateGenreCategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = (
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class NoPutViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
