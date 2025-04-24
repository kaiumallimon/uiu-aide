import traceback
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.supabase.supabase_client import supabase
from apps.llm.gemini import embedding_model, llm
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

FAISS_DIR = "faiss_indexes"


class ChatWithAgentView(APIView):
    def post(self, request):
        try:
            # Validate required fields
            agent_id = request.data.get("agent_id")
            query = request.data.get("query")

            if not agent_id:
                return Response(
                    {"error": "agent_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not query:
                return Response(
                    {"error": "query is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch agent data with error handling
            try:
                response = supabase.table("agents").select("*").eq("id", agent_id).single().execute()
                agent_data = response.data
            except Exception as e:
                return Response(
                    {
                        "error": "Failed to fetch agent data",
                        "details": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if not agent_data:
                return Response(
                    {"error": f"Agent with ID {agent_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate agent configuration
            namespace = agent_data.get("vector_namespace")
            if not namespace:
                return Response(
                    {"error": "Agent configuration error: missing vector_namespace"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            system_prompt = agent_data.get("prompt_template", "")
            if not system_prompt:
                return Response(
                    {"error": "Agent configuration error: missing prompt_template"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate prompt template structure
            if "{context}" not in system_prompt or "{question}" not in system_prompt:
                return Response(
                    {
                        "error": "Invalid prompt template",
                        "details": "Template must contain {context} and {question} placeholders"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Load FAISS index with validation
            index_path = os.path.join(FAISS_DIR, namespace)
            if not os.path.exists(index_path):
                return Response(
                    {
                        "error": "Agent knowledge base not found",
                        "details": f"No FAISS index at {index_path}"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                faiss_index = FAISS.load_local(
                    index_path,
                    embedding_model,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                return Response(
                    {
                        "error": "Failed to load agent knowledge base",
                        "details": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Create prompt template
            try:
                prompt_template = PromptTemplate(
                    template=system_prompt,
                    input_variables=["context", "question"]
                )
            except Exception as e:
                return Response(
                    {
                        "error": "Invalid prompt template configuration",
                        "details": str(e)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create and execute QA chain
            try:
                qa = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=faiss_index.as_retriever(search_kwargs={"k": 3}),
                    chain_type_kwargs={
                        "prompt": prompt_template,
                        "document_prompt": PromptTemplate(
                            input_variables=["page_content"],
                            template="{page_content}"
                        )
                    },
                    return_source_documents=True
                )

                result = qa({"query": query})

                if not result.get("result"):
                    return Response(
                        {"error": "No response generated by the agent"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                return Response({
                    "response": result["result"],
                    "sources": [doc.metadata for doc in result.get("source_documents", [])]
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {
                        "error": "Failed to generate response",
                        "details": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            # This is a last resort catch-all for unexpected errors
            error_id = str(uuid.uuid4())[:8]  # Generate a short error ID for tracking
            print(f"Error ID {error_id} in ChatWithAgentView: {str(e)}\n{traceback.format_exc()}")
            return Response(
                {
                    "error": "An unexpected error occurred",
                    "error_id": error_id,
                    "support_reference": f"REF-{error_id}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )