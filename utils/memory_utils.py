from langchain.memory import ConversationBufferMemory
from .message_converter import convert_to_langchain_messages

def initialize_memory_from_history(history: list):
    messages = convert_to_langchain_messages(history)

    memory = ConversationBufferMemory(return_messages=True)
    for msg in messages:
        memory.chat_memory.add_message(msg)
    return memory