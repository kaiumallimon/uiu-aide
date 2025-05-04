# from uuid import uuid4
# import datetime
# from config.supabase.supabase_client import supabase 
# from apps.llm.gemini import embedding_model, chat_llm  
# from utils.memory_utils import get_buffer_memory, build_prompt_from_memory_chunks  
# from config import settings
# import pinecone

# # Initialize Pinecone
# pinecone.init(
#     api_key=settings.PINECONE_API_KEY,
#     environment=settings.PINECONE_ENVIRONMENT
# )

# pinecone_index = pinecone.Index(settings.PINECONE_INDEX_NAME)

# def create_conversation(user_id: str, agent_id: str, title: str):
#     current_time = datetime.datetime.now().isoformat()
#     response = supabase.table('conversations').insert({
#         'user_id': user_id,
#         'agent_id': agent_id,
#         'title': title,
#         'created_at': current_time,
#         'updated_at': current_time,
#     }).execute()
#     result = response.model_dump()
#     if result.get("error"):
#         raise Exception(f"Failed to create conversation: {result['error']}")
#     return result.get("data")[0]

# def store_message_pinecone(conversation_id, user_id, agent_id, role, content, timestamp):
#     embedding = embedding_model.embed_documents([content])[0]
#     metadata = {
#         'conversation_id': conversation_id,
#         'user_id': user_id,
#         'agent_id': agent_id,
#         'role': role,
#         'content': content,
#         'timestamp': timestamp.isoformat()
#     }
#     pinecone_index.upsert(vectors=[{
#         'id': str(uuid4()),
#         'values': embedding,
#         'metadata': metadata
#     }])

# def store_message_db(conversation_id, user_id, role, content, timestamp):
#     response = supabase.table("messages").insert({
#         "conversation_id": conversation_id,
#         "user_id": user_id,
#         "role": role,
#         "content": content,
#         "created_at": timestamp.isoformat()
#     }).execute()
#     if response.model_dump().get("error"):
#         raise Exception("Failed to store message in Supabase")

# def chat_service(agent_id: str, user_id: str, conversation_id: str | None, user_input: str, top_k: int = 5):
#     timestamp = datetime.datetime.now()

#     if conversation_id is None:
#         conversation = create_conversation(user_id, agent_id, title=user_input[:50])
#         conversation_id = conversation["id"]

#     store_message_db(conversation_id, user_id, "user", user_input, timestamp)
#     store_message_pinecone(conversation_id, user_id, agent_id, "user", user_input, timestamp)

#     user_input_embedding = embedding_model.embed_documents([user_input])[0]
#     results = pinecone_index.query(
#         vector=user_input_embedding,
#         top_k=top_k,
#         include_metadata=True,
#         filter={
#             "user_id": {"$eq": user_id},
#             "agent_id": {"$eq": agent_id},
#             "conversation_id": {"$eq": conversation_id},
#         }
#     )
#     memory_chunks = [match['metadata']['content'] for match in results['matches']]
#     buffer_memory = get_buffer_memory(conversation_id, user_id, limit=5)

#     full_context = build_prompt_from_memory_chunks(memory_chunks, buffer_memory, user_input)
#     assistant_response = chat_llm(full_context)

#     store_message_db(conversation_id, user_id, "assistant", assistant_response, timestamp)
#     store_message_pinecone(conversation_id, user_id, agent_id, "assistant", assistant_response, timestamp)

#     return {
#         "conversation_id": conversation_id,
#         "response": assistant_response
#     }
