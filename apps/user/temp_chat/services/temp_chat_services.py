from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from apps.llm.gemini import llm
from .agent_retriever_service import get_relevant_documents_from_pinecone
from config.supabase.supabase_client import supabase
from langchain.schema import Document

def get_system_prompt_from_supabase(agent_id: str) -> str | None:
    response = (
        supabase.table("agents")
        .select("system_prompt")
        .eq("id", agent_id)
        .limit(1)
        .execute()
    )

    if response.data and len(response.data) > 0:
        return response.data[0]["system_prompt"]
    else:
        return None


def temporary_chat_with_agent(user_input: str, agent_id: str):
    """
    Chat with an agent using a custom RAG pipeline (not RetrievalQA).
    """
    # Step 1: Get system prompt
    system_prompt = get_system_prompt_from_supabase(agent_id)
    if system_prompt is None:
        raise ValueError("No data found with given agent ID.")

    # Step 2: Get relevant documents from Pinecone
    matches = get_relevant_documents_from_pinecone(user_input, agent_id)

    print("\n--- Retrieved Matches from Pinecone ---")
    print(matches)

    # Convert Pinecone matches to LangChain Document objects
    documents = [
        Document(
            page_content=match['metadata'].get('content', ''),
            metadata=match['metadata']
        )
        for match in matches
    ]

    print("\n--- Retrieved Documents ---")
    for i, doc in enumerate(documents):
        print(f"[Doc {i + 1}]:")
        print(doc.page_content)
        print("-" * 50)

    # Step 3: Format prompt manually
    context = "\n".join([doc.page_content for doc in documents])
    template = system_prompt + "\n\nContext & Previous Mid term questions:\n{context}\n\nUser Query:\n{question}\n\nAnswer:"
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    formatted_prompt = prompt.format(context=context, question=user_input)



    # Step 4: Send to Gemini LLM
    response = llm.invoke(formatted_prompt)


    # convert documents to a dictionary 
    converted_documents = []
    for doc in documents:
        doc_dict = {key: value for key, value in doc}
        converted_documents.append(doc_dict)

    print("\nLLM Response:", response.content)
    return {
        # "formatted_prompt": formatted_prompt,
        "response": response.content,
        "vector_search_result": converted_documents,
    }