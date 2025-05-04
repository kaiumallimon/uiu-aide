from config.supabase.supabase_client import supabase

def get_system_prompt_from_supabase(agent_id: str) -> str | None:
    response = (
        supabase.table("agents")
        .select("system_prompt")
        .eq("id", agent_id)
        .limit(1)
        .execute()
    )

    if response.data and len(response.data) > 0:
        return response.data[0]["system_prompt"]
    else:
        return None
