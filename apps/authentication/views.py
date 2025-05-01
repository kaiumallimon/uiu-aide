from django.shortcuts import render
from apps.authentication.serializers.auth_serializer import RegisterSerializer, LoginSerializer
from apps.authentication.services.auth_services import register, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
                        {
                            "status": "success",
                            "message": "User logged in successfully",
                            "user": response
                        },
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
