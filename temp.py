# from google import genai
# from google.genai import types
# client = genai.Client(api_key="AIzaSyDwegVVcXdRymQG9A3j403KGEzp-PFQ5h0")
# chat = client.chats.create(model="gemini-2.0-flash")

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     config=types.GenerateContentConfig(
#         system_instruction="You are a cat. Your name is Neko."),
#     contents="Hello there"
# )

# print(response.text)
# # response = chat.send_message_stream("How many paws are in my house?")
# # for chunk in response:
# #     print(chunk.text, end="")

# # for message in chat.get_history():
# #     print(f'role - {message.role}', end=": ")
# #     print(message.parts[0].text)