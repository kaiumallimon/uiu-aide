from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.temp_chat_services import temporary_chat_with_agent
from rest_framework.permissions import IsAuthenticated
from middlwares.auth_middleware import SupabaseJWTAuthentication

class TemporaryChatView(APIView):
    
    # authenticate first:
    authentication_classes = [SupabaseJWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def post(self, request):
        try:
            # retrieve data from the request
            message = request.data.get('message')
            agent_id = request.data.get('agent_id')

            # validate the data
            if not message or not agent_id:
                return Response({"error": "Message and agent_id are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Call the temporary chat service
            response = temporary_chat_with_agent(message, agent_id)

            print(response)


            return Response({
                "status": "success",
                "data": response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



