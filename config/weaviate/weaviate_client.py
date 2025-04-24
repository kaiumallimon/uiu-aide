# import weaviate
# from weaviate.auth import AuthApiKey
# from config import settings
#
# # Initialize the Weaviate client with proper authentication
# client = weaviate.Client(
#     url=f"https://{settings.WEAVIATE_URL}",  # Ensure the URL includes the scheme
#     auth_client_secret=AuthApiKey(api_key=settings.WEAVIATE_API_KEY),
#     additional_headers={
#         'X-OpenAI-Api-key': settings.GEMINI_API_KEY  # Replace with your OpenAI API key
#     }
# )
