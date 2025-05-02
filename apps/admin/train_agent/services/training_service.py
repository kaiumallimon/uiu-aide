from typing import List, Dict, Any
from django.core.files.uploadedfile import UploadedFile
from utils.extract_pdf_text_and_chunk import extract_text_from_pdf, extract_questions, extract_header, clean_text, create_chunked_output
from utils.flatten_and_chunk import flatten_and_chunk_questions
from apps.llm.gemini import embedding_model
from apps.admin.train_agent.services.store_embed_to_db import save_training_data_to_pinecone_db
from config.supabase.supabase_client import supabase  # Still used for document metadata

def train_agent(agent_id: str, pdf_file: UploadedFile) -> Dict[str, Any]:
    # Step 1: Extract and clean raw text
    text = extract_text_from_pdf(pdf_file)
    text = clean_text(text)

    # Step 2: Extract metadata and questions
    header = extract_header(text)
    questions = extract_questions(text)

    # Step 3: Flatten and chunk the question data
    question_chunks = create_chunked_output(header, questions)

    # Step 4: Extract only the "content" field for embedding
    question_texts = [chunk["content"] for chunk in question_chunks]

    # Generate embeddings
    embeddings = embedding_model.embed_documents(question_texts)

    if len(question_texts) != len(embeddings):
        raise ValueError("Mismatch between number of chunks and embeddings.")

        # Step 5: Prepare data for Pinecone
    pinecone_data = []
    trimester = header.get("trimester", "").replace(" ", "_")
    course_code = header.get("course_code", "").replace(" ", "_")

    for idx, chunk in enumerate(question_chunks):
        # Prepare metadata for each chunk
        metadata = {
            "question_id": chunk["question_id"],
            "agent_id": agent_id,
            "trimester": header.get("trimester", ""),
            "course_code": header.get("course_code", ""),
            "course_title": header.get("course_title", ""),
            "content": chunk["content"]
        }

        # Create unique ID using trimester, course_code, question_id, and index
        unique_id = f"{trimester}-{course_code}-{chunk['question_id']}-{idx}"

        # Create Pinecone-compatible data structure
        pinecone_data.append({
            "id": unique_id,
            "values": embeddings[idx],
            "metadata": metadata
        })


    # Step 6: Store embeddings in Pinecone
    save_training_data_to_pinecone_db(
        agent_id=agent_id,
        pinecone_data=pinecone_data
    )

    # Step 6: Return summary
    return {
        "agent_id": agent_id,
        "header": header,
        "questions": questions,
        "chunk_count": len(question_chunks),
        "embedding_count": len(embeddings),
        "embedding_dim": len(embeddings[0]) if embeddings else 0,
        "embeddings": embeddings,
    }
