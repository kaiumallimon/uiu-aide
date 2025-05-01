from django.urls import path
from apps.user.temp_chat.views import TemporaryChatView

urlpatterns = [
    path('', TemporaryChatView.as_view(), name='register'),
]
