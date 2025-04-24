from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.get("role") == "admin"


"""
# example usage in a view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.authentication.middleware.supabase_auth import SupabaseAuth
from apps.authentication.permissions import IsAdmin


class AdminOnlyView(APIView):
    authentication_classes = [SupabaseAuth]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({
            "message": f"Welcome admin {request.user['email']}",
            "role": request.user["role"]
        })
"""