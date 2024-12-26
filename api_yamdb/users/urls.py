from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, signup, token


v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', signup),
    path('auth/token/', token),
]
