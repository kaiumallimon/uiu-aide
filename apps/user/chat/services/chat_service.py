from uuid import uuid4
import datetime
from config.supabase.supabase_client import supabase
from apps.llm.gemini import embedding_model, llm
from config import settings
from pinecone import Pinecone
import numpy as np
from utils.flatten_and_chunk import chunk_text

# Initialize Pinecone
pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)
pinecone_index = pinecone.Index("uiu-aide")


def create_conversation(user_id: str, agent_id: str, title: str):
    id = str(uuid4())
    current_time = datetime.datetime.now().isoformat()
    response = (
        supabase.table("conversations")
        .insert(
            {
                "id": id,
                "user_id": user_id,
                "agent_id": agent_id,
                "title": title,
                "created_at": current_time,
                "updated_at": current_time,
            }
        )
        .execute()
    )
    result = response.model_dump()
    if result.get("error"):
        raise Exception(f"Failed to create conversation: {result['error']}")
    return result.get("data")[0]


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
        print(
            f"Successfully upserted {len(pinecone_data)} items into Pinecone index '{settings.PINECONE_INDEX_NAME}'."
        )
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


def store_message_db(message_id, conversation_id, role, content):
    current_time = datetime.datetime.now().isoformat()
    response = (
        supabase.table("messages")
        .insert(
            {
                "id": message_id,
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "timestamp": current_time,
            }
        )
        .execute()
    )

    if response.model_dump().get("error"):
        raise Exception("Failed to store message in Supabase")

    return response.model_dump().get("data")[0]


def get_relevant_messages_from_pinecone(
    conversation_id: str,
    user_id: str,
    agent_id: str,
    query_embedding: list,
    top_k: int = 5,
):
    try:
        query_response = pinecone_index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={
                "conversation_id": conversation_id,
                "agent_id": agent_id,
            },
        )

        print(f"Query response: {query_response}")  # This will print the raw response

        if query_response and "matches" in query_response:
            relevant_messages = []
            for match in query_response["matches"]:
                # Check the structure of the match and metadata
                print(f"Match metadata: {match['metadata']}")  # Check if the metadata is valid

                relevant_messages.append(
                    {
                        "conversation_id": match["metadata"]["conversation_id"],
                        "user_id": match["metadata"]["user_id"],
                        "agent_id": match["metadata"]["agent_id"],
                        "role": match["metadata"]["role"],
                        "content": match["metadata"]["content"],
                        "created_at": match["metadata"]["created_at"],
                    }
                )
            return relevant_messages
        else:
            raise ValueError("No relevant messages found in Pinecone response")

    except Exception as e:
        raise ValueError(f"Failed to retrieve relevant messages from Pinecone: {e}")


def message_sending_service(
    agent_id: str,
    user_id: str,
    conversation_id: str | None,
    content: str,
    role: str = "user",
):
    try:
        if conversation_id is None:
            conversation = create_conversation(user_id, agent_id, content)
            conversation_id = conversation["id"]

        message_id = str(uuid4())
        pinecone_response = store_message_pinecone(
            conversation_id, user_id, agent_id, role, content, message_id
        )

        if not pinecone_response:
            raise Exception("Failed to store message in Pinecone")

        db_response = store_message_db(message_id, conversation_id, role, content)

        if not db_response:
            raise Exception("Failed to store message in Supabase")

        relevant_messages = get_relevant_messages_from_pinecone(
            conversation_id, user_id, agent_id, pinecone_response["embedding"]
        )

        print(f"Relevant messages: {relevant_messages}")

        return {
            "conversation_id": conversation_id,
            "stored_message": db_response,
            "relevant_context": relevant_messages,
        }

    except Exception as e:
        raise Exception(f"Error in message_sending_service: {e}")
