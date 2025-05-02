from typing import List
from langchain.schema import Document
from apps.llm.gemini import embedding_model
from pinecone import Pinecone
from config import settings

def get_relevant_documents_from_pinecone(query: str, agent_id: str, k: int = 5) -> List[Document]:
    """
    Retrieve top-k relevant documents from Pinecone for the given query and agent ID.
    """

    try:
        # initialize pinecone
        pinecone = Pinecone(
        api_key = settings.PINECONE_API_KEY
        )

        index_name = "uiu-aide"

        if not pinecone.has_index(name=index_name):
            raise ValueError(f"Index {index_name} does not exist.")

        index = pinecone.Index(index_name)


        # Step 1: Embed the query
        query_embedding = embedding_model.embed_query(query)

        # Step 2: Query Pinecone index with metadata filter for this agent
        query_result = index.query(vector=query_embedding, top_k=k, include_metadata=True,)

        return query_result["matches"]

    except Exception as e:
        raise ValueError(f"Failed to retrieve documents from Pinecone: {e}")

    
