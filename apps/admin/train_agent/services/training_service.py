from typing import List, Dict, Any
from django.core.files.uploadedfile import UploadedFile
from utils.extract_pdf_text import extract_text_from_pdf, extract_questions, extract_header, clean_text
from  utils.flatten_and_chunk import flatten_and_chunk_questions
from apps.llm.gemini import embedding_model
from apps.admin.train_agent.services.store_embed_to_db import save_training_data_to_db

def train_agent(agent_id: str, pdf_file: UploadedFile):
    text = extract_text_from_pdf(pdf_file)  # Now handles file-like object
    text = clean_text(text)
    header = extract_header(text)  # Pass text, not file
    questions = extract_questions(text)

    # Flatten and chunk the questions
    question_chunks = flatten_and_chunk_questions(questions)

    # Ensure that question_chunks is a list of strings
    question_chunks = [str(chunk) for chunk in question_chunks]

    # now embed the chunks (part of embedding pipeline)
    embeddings = embedding_model.embed_documents(question_chunks)

    # now store the chunks and embeddings in the database
    save_training_data_to_db(
        agent_id=agent_id,
        filename=pdf_file.name,
        raw_text=text,
        chunks=question_chunks,
        embeddings=embeddings
    )

    return {
        "agent_id": agent_id,
        "header": header,
        "questions": questions,
        "chunk_count": len(question_chunks),
        "embedding_count": len(embeddings)
    }