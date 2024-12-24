# from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers

from .views import AuthViewSet, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('auth', AuthViewSet, basename='auth')


urlpatterns = [
    path('', include(v1_router.urls)),
    # path('auth/signup/', UserCreate.as_view()),
    # path('auth/token/', auth_views.PasswordChangeView.as_view()),
]
