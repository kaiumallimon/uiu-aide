import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.supabase.supabase_client import supabase
from apps.llm.gemini import embedding_model
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.schema.document import Document
from uuid import uuid4
import os

FAISS_DIR = "faiss_indexes"  # Directory to save agent vector indexes

class CreateAgentView(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            prompt = request.data.get("prompt_template")
            tools = request.data.get("tools", [])
            documents = request.data.get("documents", [])
            created_by = request.data.get("created_by")

            # Step 1: Generate UUID for namespace (used as FAISS file name)
            namespace = str(uuid4())

            # Step 2: Split text into chunks
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            all_docs = []
            for doc in documents:
                chunks = text_splitter.split_text(doc["text"])
                for chunk in chunks:
                    all_docs.append(Document(page_content=chunk, metadata={"namespace": namespace}))

            # Step 3: Embed and store in FAISS
            faiss_index = FAISS.from_documents(all_docs, embedding_model)

            # Create directory if not exists
            os.makedirs(FAISS_DIR, exist_ok=True)
            index_path = os.path.join(FAISS_DIR, f"{namespace}")

            # Save FAISS index and metadata
            faiss_index.save_local(index_path)

            # Step 4: Save agent metadata in Supabase
            supabase.table("agents").insert({
                "name": name,
                "prompt_template": prompt,
                "tools": tools,
                "vector_namespace": namespace,
                "created_by": created_by,
            }).execute()

            return Response({"message": "Agent created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error occurred:", e)
            print("Traceback:", traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
