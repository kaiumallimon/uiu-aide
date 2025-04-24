from django.urls import  path
from apps.chat.views import ChatWithAgentView

urlpatterns = [
    path('chat/', ChatWithAgentView.as_view(), name='chat_with_agent'),
]