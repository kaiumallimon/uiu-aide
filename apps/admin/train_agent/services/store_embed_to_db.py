import uuid
from datetime import datetime
from typing import List
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_core.documents import Document
from apps.llm.gemini import embedding_model
from config.supabase.supabase_client import supabase
from config.pinecone_.pinecone_client import pinecone_index


def save_training_data_to_db_with_pinecone(
        agent_id: str,
        filename: str,
        raw_text: str,
        chunks: List[str],
        embeddings: List[List[float]]
):
    # Step 1: Insert raw document metadata to Supabase
    document_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()

    document_data = {
        "id": document_id,
        "agent_id": agent_id,
        "filename": filename,
        "content": raw_text,
        "created_at": created_at
    }

    doc_response = supabase.table("documents").insert(document_data).execute()

    if hasattr(doc_response, 'error') and doc_response.error:
        raise Exception(f"Failed to insert document: {doc_response.error}")

    # Step 2: Prepare documents for Pinecone
    documents = [
        Document(
            page_content=chunk,
            metadata={
                "document_id": document_id,
                "agent_id": agent_id,
                "filename": filename,
                "text": chunk  # Important for retrieval
            }
        )
        for chunk in chunks
    ]

    # Step 3: Store embeddings in Pinecone
    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embedding_model,
        index_name="uiu-aide"
    )

    return {"document_id": document_id}