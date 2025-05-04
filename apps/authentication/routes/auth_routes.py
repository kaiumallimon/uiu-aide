from django.urls import path
from apps.authentication.views import RegisterView, LoginView, RefreshTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/',RefreshTokenView.as_view(), name='refresh_token')
]
