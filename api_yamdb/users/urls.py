from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserCreate


urlpatterns = [
    path('auth/signup/', UserCreate.as_view()),
    path('auth/token/', auth_views.PasswordChangeView.as_view()),
]