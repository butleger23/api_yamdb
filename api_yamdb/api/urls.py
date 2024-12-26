from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (
    TitleViewSet, ReviewViewSet, CommentViewSet
)


router = DefaultRouter()
# предлагаю сюда остальное по жанрам и категориям
router.register(r'titles', TitleViewSet, basename='title')

title_router = NestedDefaultRouter(router, r'titles', lookup='title')
title_router.register(r'reviews', ReviewViewSet, basename='title-reviews')

review_router = NestedDefaultRouter(title_router, r'reviews', lookup='review')
review_router.register(
    r'comments',
    CommentViewSet,
    basename='title-review-comments'
)


api_version_prefix = 'v1/'


urlpatterns = [
    path(api_version_prefix, include([
        path('', include(router.urls)),
        path('', include(title_router.urls)),
        path('', include(review_router.urls)),
        # предлагаю users.urls сюда
    ]))
]
