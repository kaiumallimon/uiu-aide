from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.memory import ConversationBufferMemory


# Load environment variables from .env file
load_dotenv()


search = TavilySearchResults(max_results=2)

@tool 
def get_current_time() -> str:
    """Get the current time."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def reverse_text(text: str) -> str:
    """Reverses the given text string."""
    return text[::-1]


@tool
def get_weather(query: str) -> str:
    """Fetch weather information using TavilySearchResults"""
    query_lower = query.lower()
    
    # Check if the query mentions 'weather' and a location like 'dhaka'
    if "weather" in query_lower and ("dhaka" in query_lower or "bangladesh" in query_lower):
        search = TavilySearchResults(max_results=2)
        search_results = search.invoke(query)
        
        if search_results:
            return f"The current weather in Dhaka is: {search_results[0]['content']}"
        return "Sorry, I couldn't retrieve the weather information."
    
    return "No weather-related query detected."


tools = [get_weather, get_current_time, reverse_text]

model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
)

memory = ConversationBufferMemory(return_messages=True)


# Create the agent with tools
agent_executor = create_react_agent(model, tools)

while True:
    # Get query from the terminal
    user_input = input("Ask something: ")

    # Break the loop if the user wants to exit
    if user_input.lower() == "exit":
        print("Exiting the program...")
        break

    # Interact with the model and tools
    for step in agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
