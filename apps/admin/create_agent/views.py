import traceback
from rest_framework.views import APIView
from .services.agent_creation_service import create_agent_service
from rest_framework.response import Response
from rest_framework import status


class CreateAgentView(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            name = request.data.get("name")
            prompt = request.data.get("system_prompt")
            description = request.data.get("description")
            created_by = request.data.get("created_by")

            # create the agent in the database
            response = create_agent_service(
                name=name,
                description=description,
                system_prompt=prompt,
                created_by=created_by
            )

            # Return the response
            return Response(
                {
                    "status": "success",
                    "message": "Agent created successfully",
                    "agent": response
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Log the error
            print(f"Error creating agent: {e}")
            traceback.print_exc()

            # Return an error response
            return Response(
                {
                    "status": "error",
                    "message": "Agent creation failed",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )