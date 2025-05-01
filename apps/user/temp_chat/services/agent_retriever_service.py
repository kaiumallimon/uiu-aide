from typing import List
from langchain.schema import Document
from apps.llm.gemini import embedding_model
from config.pinecone_.pinecone_client import pinecone_index as index


def get_relevant_documents_from_pinecone(query: str, agent_id: str, k: int = 5) -> List[Document]:
    """
    Retrieve top-k relevant documents from Pinecone for the given query and agent ID.
    """
    # Step 1: Embed the query
    query_embedding = embedding_model.embed_query(query)

    # Step 2: Query Pinecone index with metadata filter for this agent
    response = index.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True,
        filter={"agent_id": {"$eq": agent_id}}
    )

    # Step 3: Convert Pinecone matches to LangChain Document objects
    docs = []
    for match in response["matches"]:
        metadata = match["metadata"]
        content = metadata.get("text") or metadata.get("chunk") or ""
        docs.append(Document(page_content=content, metadata=metadata))

    return docs
