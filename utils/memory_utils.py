from collections import deque
from typing import List, Dict

# In-memory buffer (replace with Redis for scalability)
memory_buffers = {}

def init_buffer_memory(conversation_id: str, max_length: int = 10):
    """
    Initialize a buffer memory for a conversation.
    """
    memory_buffers[conversation_id] = deque(maxlen=max_length)

def get_buffer_memory(conversation_id: str) -> List[Dict]:
    """
    Retrieve recent messages from buffer.
    """
    return list(memory_buffers.get(conversation_id, []))

def update_buffer_memory(conversation_id: str, message: Dict):
    """
    Append a message to buffer memory.
    """
    if conversation_id not in memory_buffers:
        init_buffer_memory(conversation_id)
    memory_buffers[conversation_id].append(message)
