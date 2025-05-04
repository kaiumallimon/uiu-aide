from config import settings
from pinecone import Pinecone


# Initialize Pinecone
pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)
pinecone_index = pinecone.Index("uiu-aide")



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

        # print(f"Query response: {query_response}")  # This will print the raw response

        if query_response and "matches" in query_response:
            relevant_messages = []
            for match in query_response["matches"]:
                # Check the structure of the match and metadata
                # print(
                #     f"Match metadata: {match['metadata']}"
                # )  # Check if the metadata is valid

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
