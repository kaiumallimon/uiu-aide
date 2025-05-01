from typing import List, Dict, Any
from django.core.files.uploadedfile import UploadedFile
from utils.extract_pdf_text import extract_text_from_pdf, extract_questions, extract_header, clean_text
from utils.flatten_and_chunk import flatten_and_chunk_questions
from apps.llm.gemini import embedding_model
from apps.admin.train_agent.services.store_embed_to_db import save_training_data_to_db_with_pinecone
from config.supabase.supabase_client import supabase  # Still used for document metadata

def train_agent(agent_id: str, pdf_file: UploadedFile) -> Dict[str, Any]:
    # Step 1: Extract and clean raw text
    text = extract_text_from_pdf(pdf_file)
    text = clean_text(text)

    # Step 2: Extract metadata and questions
    header = extract_header(text)
    questions = extract_questions(text)

    # Step 3: Flatten and chunk the question data
    question_chunks = flatten_and_chunk_questions(questions)

    # Step 4: Generate embeddings
    embeddings = embedding_model.embed_documents(question_chunks)

    if len(question_chunks) != len(embeddings):
        raise ValueError("Mismatch between number of chunks and embeddings.")

    # Step 5: Store in Pinecone instead of Supabase
    save_training_data_to_db_with_pinecone(
        agent_id=agent_id,
        filename=pdf_file.name,
        raw_text=text,
        chunks=question_chunks,
        embeddings=embeddings
    )

    # Step 6: Return summary
    return {
        "agent_id": agent_id,
        "header": header,
        "questions": questions,
        "chunk_count": len(question_chunks),
        "embedding_count": len(embeddings)
    }
