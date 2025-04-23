from django.urls import path
from apps.test_users.views import UserListCreateView

urlpatterns = [
    path('all/', UserListCreateView.as_view(),name='get-users'),
    path('create/', UserListCreateView.as_view(),name='create-user'),
]