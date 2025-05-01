import uuid
from datetime import datetime
from config.supabase.supabase_client import supabase


# def create_vectorstore(agent_id: str):
#     """
#     Creates a vector store for the agent and returns its ID.
#     """
#     try:
#         vectorstore_id = str(uuid.uuid4())
#
#         vectorstore_data = {
#             "id": vectorstore_id,
#             "agent_id": agent_id,
#             "created_at": datetime.now().isoformat()
#         }
#
#         response = supabase.table("vectorstores").insert(vectorstore_data).execute()
#         result = response.model_dump()  # Safely convert to dictionary
#
#         if result.get("error"):
#             raise Exception(f"Vectorstore creation failed: {result['error']}")
#
#         return vectorstore_id
#
#     except Exception as e:
#         print(str(e))
#         raise e


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

        # # vectorstore_id = create_vectorstore(agent_id)
        #
        # updated_agent_data = {
        #     "vectorstore_id": vectorstore_id,
        # }

        # update_response = supabase.table("agents").update(updated_agent_data).eq("id", agent_id).execute()
        # update_result = update_response.model_dump()

        # print("Update result:", update_result)
        #
        # if update_result.get("error"):
        #     raise Exception(f"Failed to update agent with vectorstore_id: {update_result['error']}")

        return agent_result.get("data")[0]


    except Exception as e:
        return {
            "status": "error",
            "message": "Agent creation failed",
            "error": str(e)
        }
