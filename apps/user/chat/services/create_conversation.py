from uuid import uuid4
import datetime
from config.supabase.supabase_client import supabase
from config import settings
from pinecone import Pinecone

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
