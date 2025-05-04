import datetime
from apps.llm.gemini import embedding_model
from config import settings
from pinecone import Pinecone
import numpy as np
from utils.flatten_and_chunk import chunk_text


# Initialize Pinecone
pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)
pinecone_index = pinecone.Index("uiu-aide")


def store_message_pinecone(
    conversation_id: str,
    user_id: str,
    agent_id: str,
    role: str,
    content: str,
    message_id: str,
):
    chunks = chunk_text(content)
    embeddings = embedding_model.embed_documents(chunks)

    pinecone_data = []
    timestamp = datetime.datetime.now()

    for idx, chunk in enumerate(chunks):
        unique_id = f"{conversation_id}-{user_id}-{agent_id}-{message_id}-{idx}"
        pinecone_data.append(
            {
                "id": unique_id,
                "values": embeddings[idx],
                "metadata": {
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    "agent_id": agent_id,
                    "role": role,
                    "content": chunk,
                    "created_at": timestamp.isoformat(),
                },
            }
        )

    try:
        pinecone_index.upsert(vectors=pinecone_data)
        # print(
        #     f"Successfully upserted {len(pinecone_data)} items into Pinecone index '{settings.PINECONE_INDEX_NAME}'."
        # )
        combined_embedding = np.mean(embeddings, axis=0).tolist()

        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "agent_id": agent_id,
            "role": role,
            "content": content,
            "created_at": timestamp.isoformat(),
            "embedding": combined_embedding,
        }
    except Exception as e:
        raise ValueError(f"Failed to upsert data into Pinecone: {e}")
