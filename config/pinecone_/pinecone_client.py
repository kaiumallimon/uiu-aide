from pinecone import Pinecone
from config import settings

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Get the Pinecone index
pinecone_index = pc.Index("uiu-aide")