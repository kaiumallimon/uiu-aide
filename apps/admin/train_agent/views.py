from rest_framework.response import Response
from rest_framework import status
import traceback
from rest_framework.views import APIView
from .services.training_service import train_agent

class AgentTrainingView(APIView):
    def post(self, request):
        try:
            agent_id = request.data.get("agent_id")
            pdf_file = request.FILES.get("pdf_file")  # ✅ Corrected here

            print(f"Received agent_id: {agent_id}")
            print(f"Received pdf_file: {pdf_file}")

            if agent_id is None or pdf_file is None:
                return Response(
                    {
                        "status": "error",
                        "message": "Agent ID and PDF file are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Call the training service
            response = train_agent(agent_id=agent_id, pdf_file=pdf_file)

            return Response(
                {
                    "status": "success",
                    "message": "Agent trained successfully",
                    "data": response
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Error training agent: {e}")
            traceback.print_exc()
            return Response(
                {
                    "status": "error",
                    "message": "Agent training failed",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
