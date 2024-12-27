from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import (
    TitleViewSet, ReviewViewSet, CommentViewSet,
    CategoryViewSet, GenreViewSet
)
from users.views import UserViewSet, token, signup


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='title')
router.register('users', UserViewSet, basename='users')

title_router = NestedDefaultRouter(router, 'titles', lookup='title')
title_router.register('reviews', ReviewViewSet, basename='title-reviews')

review_router = NestedDefaultRouter(title_router, 'reviews', lookup='review')
review_router.register(
    'comments',
    CommentViewSet,
    basename='title-review-comments'
)

api_version_prefix = 'v1/'

urlpatterns = [
    path(api_version_prefix, include([
        path('', include(router.urls)),
        path('', include(title_router.urls)),
        path('', include(review_router.urls)),
        path('auth/token/', token),
        path('auth/signup/', signup),
    ]))
]
