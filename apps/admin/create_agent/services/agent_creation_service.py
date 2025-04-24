# from apps.admin.create_agent.models.agent_model import Agent, Tool
# from apps.admin.tools.pdf_read_embedd.read_pdf import embed_and_store_pdf_in_weaviate
# from django.contrib.auth.models import User
#
# def create_agent_with_tools(user_id: str, name: str, prompt_template: str, tool_names: list, pdf_path: str):
#     """
#     Create an agent with the specified name, prompt template, and tools.
#     The agent will also embed and store a PDF in Weaviate.
#
#     Args:
#         user (User): The user creating the agent.
#         name (str): The name of the agent.
#         prompt_template (str): The prompt template for the agent.
#         tool_names (list): List of tool names to associate with the agent.
#         pdf_path (str): Path to the PDF file to be embedded and stored in Weaviate.
#
#     Returns:
#         Agent: The created agent instance.
#     """
#     # Create the agent:
#
#     namespace = f"{user_id}_{name.replace(' ', '_').lower()}"
#
#     # Step 1: Embed and store in weaviate
