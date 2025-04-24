from django.urls import path
from apps.admin.create_agent.views import CreateAgentView

urlpatterns = [
    path('create/', CreateAgentView.as_view(), name='create-agent'),
]