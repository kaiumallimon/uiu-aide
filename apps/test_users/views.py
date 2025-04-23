from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.test_users.services.user_services import get_all_users, create_user
from apps.test_users._models.user_serializer import UserSerializer

class UserListCreateView(APIView):
    # GET: fetch all users
    def get(self, request):
        users = get_all_users()

        if users["status"] == "error":
            return Response(users, status= status.HTTP_400_BAD_REQUEST)
        

        print(f"Fetched users: {users}")
        serializer = UserSerializer(users["data"], many =True)
        return Response({
            "status": users["status"],
            "message": users["message"],
            "data": serializer.data

        }, status=status.HTTP_200_OK)
    

    # POST: create a new user
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")

        print(f"Received data: {request.data}")

        if not name or not email:
            return Response({"error": "Name and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = create_user(name, email)

        print(f"User creation response: {user}")

        if user["status"] == "error":
            return Response(user, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status": user["status"],
            "message": user["message"],

        }, status=status.HTTP_201_CREATED)