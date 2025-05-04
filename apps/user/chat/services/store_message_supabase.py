
import datetime
from config.supabase.supabase_client import supabase

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
