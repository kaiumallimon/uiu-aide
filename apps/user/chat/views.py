from rest_framework import status
import traceback
from rest_framework.views import APIView
from .services.chat_service import message_sending_service
from middlwares.auth_middleware import SupabaseJWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ChatWithAgentView(APIView):
    # authenticate first:
    authentication_classes = [SupabaseJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            agent_id = request.data.get("agent_id")
            conversation_id = request.data.get("conversation_id")
            content = request.data.get("content")
            role = request.data.get("role", "user")
            
            if not all([user_id, agent_id, content]):
                return Response(
                    {"error": "Missing required fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response_data = message_sending_service(
                agent_id, user_id, conversation_id, content, role
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




