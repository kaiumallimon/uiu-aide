from config.supabase.supabase_client import supabase

def get_conversation_history(conversation_id: str, limit: int):
    try:
        response = (
            supabase.table("messages")
            .select("id, conversation_id, role, content, metadata, timestamp")
            .eq("conversation_id", conversation_id)
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )

        data = response.model_dump().get("data")
        if data is None:
            raise Exception("No data found")

        # Reverse to get oldest → newest and format like ChatGPT
        formatted_history = [
            {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"],
            }
            for msg in reversed(data)
        ]
        return formatted_history

    except Exception as e:
        raise Exception(f"Failed to retrieve conversation history: {e}")
