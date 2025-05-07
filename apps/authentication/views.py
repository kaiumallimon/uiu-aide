from django.shortcuts import render
import requests
from apps.authentication.serializers.auth_serializer import RegisterSerializer, LoginSerializer
from apps.authentication.services.auth_services import register, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config import settings

class RegisterView(APIView):
    # [POST]
    # This view handles user registration.
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                # Call the updated register function
                user_response = register(
                    full_name=data['full_name'],
                    email=data['email'],
                    password=data['password'],
                    role=data['role']
                )

                if user_response:
                    return Response(
                        {
                            "status": "success",
                            "message": "User registered successfully",
                            "user": user_response
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {
                            "status": "error",
                            "message": "User registration failed at profile creation step.",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validation failed
        return Response(
            {
                "status": "error",
                "message": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            try:
                response = login(data['email'], data['password'])

                if response is not None:
                    return Response(
                        response,
                        status=status.HTTP_200_OK
                    )
                else:
                    # got no response
                    return Response(
                        {
                            "status": "error",
                            "message": "User login failed",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "status": "error",
                "message": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(
                {"status": "error", "message": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        SUPABASE_URL = settings.SUPABASE_URL
        SUPABASE_KEY = settings.SUPABASE_SERVICE_ROLE_KEY  # Prefer service role for server-side

        try:
            response = requests.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token",
                headers={
                    "Content-Type": "application/json",
                    "apikey": SUPABASE_KEY,
                },
                json={"refresh_token": refresh_token}
            )

            if response.status_code == 200:
                data = response.json()
                return Response(
                    {"status": "success", "session": data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "error", "message": response.json()},
                    status=response.status_code
                )

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )