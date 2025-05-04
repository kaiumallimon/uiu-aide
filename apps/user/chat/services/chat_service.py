from uuid import uuid4
from apps.llm.gemini import embedding_model, llm
from utils.memory_utils import initialize_memory_from_history
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .conversation_history_retreiver import get_conversation_history
from .create_conversation import create_conversation
from .relevant_message_retreiver_pinecone import get_relevant_messages_from_pinecone
from .store_message_pinecone import store_message_pinecone
from .store_message_supabase import store_message_db
from .system_prompt_retreiver import get_system_prompt_from_supabase
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain.schema import HumanMessage, AIMessage


def message_sending_service(
    agent_id: str,
    user_id: str,
    conversation_id: str | None,
    content: str,
    role: str = "user",
):
    try:
        # Step 1: Create new conversation if needed
        if conversation_id is None:
            conversation = create_conversation(user_id, agent_id, content)
            conversation_id = conversation["id"]

        # Step 2: Store user message
        message_id = str(uuid4())
        pinecone_response = store_message_pinecone(
            conversation_id, user_id, agent_id, role, content, message_id
        )
        db_response = store_message_db(message_id, conversation_id, role, content)

        # Step 3: Retrieve relevant Pinecone memories
        relevant_messages = get_relevant_messages_from_pinecone(
            conversation_id, user_id, agent_id, pinecone_response["embedding"]
        )

        # Step 4: Load last N messages from Supabase
        conversation_history = get_conversation_history(conversation_id, limit=5)

        # Step 5: Get system prompt
        system_prompt = get_system_prompt_from_supabase(agent_id)
        if system_prompt is None:
            raise ValueError("No system prompt found for this agent.")

        # Step 6: Format history as string
        formatted_history = ""
        for msg in reversed(conversation_history):
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n"


        # Step 7: Create memory object (optional)
        memory = ConversationBufferMemory(return_messages=True)
        for msg in reversed(conversation_history):
            if msg["role"] == "user":
                memory.chat_memory.add_user_message(msg["content"])
            else:
                memory.chat_memory.add_ai_message(msg["content"])

        # Step 8: Build prompt template
        prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""
{system_prompt}

Chat History:
{history}

User: {input}
Assistant:""",
        )

        chain = LLMChain(
            llm=llm,
            prompt=prompt_template.partial(system_prompt=system_prompt),
            memory=memory,
            verbose=True,
        )

        # Step 9: Predict
        response = chain.predict(
            history=formatted_history,
            input=content,
        )

        print(f"LLM response: {response}")
        print(f"Memory: {memory.chat_memory.messages}")
        
        
        # now add the response to the memory
        memory.chat_memory.add_ai_message(response)
        
        # store the response in supabase
        message_id = str(uuid4())
        store_message_db(message_id,conversation_id, "agent", response)

        return {
            "conversation_id": conversation_id,
            "stored_message": db_response,
            "llm_response": response,
            "relevant_messages": relevant_messages,
            "formatted_history": conversation_history,
        }

    except Exception as e:
        raise Exception(f"Error in message_sending_service: {e}")
