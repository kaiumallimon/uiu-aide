import uuid
from datetime import datetime
from typing import List

from config.supabase.supabase_client import supabase


def save_training_data_to_db(
    agent_id: str,
    filename: str,
    raw_text: str,
    chunks: List[str],
    embeddings: List[List[float]]
):
    # Step 1: Create a new document entry
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
    doc_result = doc_response.model_dump()
    if doc_result.get("error"):
        raise Exception(f"Failed to insert document: {doc_response.error}")

    # Step 2: Create embedding rows for each chunk
    embedding_rows = []
    for chunk, embedding in zip(chunks, embeddings):
        if len(embedding) != 768:
            raise ValueError(f"Embedding dimension mismatch: expected 768, got {len(embedding)}")

        embedding_rows.append({
            "id": str(uuid.uuid4()),
            "document_id": document_id,
            "chunk": chunk,
            "embedding": embedding
        })

    embed_response = supabase.table("embeddings").insert(embedding_rows).execute()
    embed_result = embed_response.model_dump()
    if embed_result.get("error"):
        raise Exception(f"Failed to insert embeddings: {embed_response.error}")

    return {
        "document_id": document_id,
    }
