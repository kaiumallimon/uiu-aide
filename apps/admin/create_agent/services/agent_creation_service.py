import uuid
from datetime import datetime
from config.supabase.supabase_client import supabase


def create_agent_service(
        name: str,
        description: str,
        system_prompt: str,
        created_by: str):
    """
    Create a new agent in the database.
    """
    try:
        agent_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()

        agent_data = {
            "id": agent_id,
            "name": name,
            "description": description,
            "system_prompt": system_prompt,
            "created_by": created_by,
            "created_at": created_at,
        }

        agent_response = supabase.table("agents").insert(agent_data).execute()
        agent_result = agent_response.model_dump()

        if agent_result.get("error"):
            raise Exception(f"Failed to create agent: {agent_result['error']}")

    

        return agent_result.get("data")[0]


    except Exception as e:
        return {
            "status": "error",
            "message": "Agent creation failed",
            "error": str(e)
        }
