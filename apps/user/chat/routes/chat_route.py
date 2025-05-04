from django.urls import path
from apps.user.chat.views import ChatWithAgentView

urlpatterns = [
    path('', ChatWithAgentView.as_view(), name='chat-with-agent'),
]