from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import config.settings as settings

embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=settings.GEMINI_API_KEY)
