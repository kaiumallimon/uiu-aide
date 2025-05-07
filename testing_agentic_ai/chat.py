from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType

# Load environment variables
load_dotenv()

# Initialize model
model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
)

# Search tool instance
search = TavilySearchResults()

# Define tools using single-input pattern
@tool
def get_current_time(input: str) -> str:
    """Returns the current time (input is unused)."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def reverse_text(input: str) -> str:
    """Reverses the given text string."""
    return input[::-1]

@tool
def get_weather(input: str) -> str:
    """Fetch weather information for a given location using TavilySearchResults."""
    results = search.invoke(f"current weather in {input}")
    if results:
        return f"The current weather in {input} is: {results[0]['content']}"
    return f"Sorry, I couldn't retrieve the weather information for {input}."

# Register tools
tools = [get_current_time, reverse_text, get_weather]

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Custom system prompt
system_prompt = """
You are AIDE, a friendly, helpful AI assistant. You should be detailed, conversational, and always explain your reasoning when helpful.
If a user asks a general question, greet them first and then provide a helpful answer.
"""

# Initialize the agent
agent_executor = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={"prefix": system_prompt}
)

# Main loop
while True:
    user_input = input("Ask something (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent_executor.invoke({"input": user_input})
    # print("\nAIDE:", response["output"])
