from langchain.schema import HumanMessage, AIMessage

def convert_to_langchain_messages(chat_history: list):
    converted = []
    for msg in chat_history:
        if msg["role"] == "user":
            converted.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            converted.append(AIMessage(content=msg["content"]))
        # You can add more roles if needed
    return converted
