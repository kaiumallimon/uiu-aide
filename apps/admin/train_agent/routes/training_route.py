from django.urls import path
from apps.admin.train_agent.views import AgentTrainingView

urlpatterns = [
    path('', AgentTrainingView.as_view(), name='train-agent'),
]