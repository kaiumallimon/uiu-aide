from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from apps.llm.gemini import llm
from .agent_retriever_service import get_relevant_documents_from_pinecone
from config.supabase.supabase_client import supabase


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
    Chat with an agent using a RAG system powered by Pinecone vector search.
    """
    # Step 1: Get system prompt
    system_prompt = get_system_prompt_from_supabase(agent_id)
    if system_prompt is None:
        raise ValueError("No data found with given agent ID.")

    # Step 2: Get relevant documents from Pinecone
    docs = get_relevant_documents_from_pinecone(user_input, agent_id)

    print("\n--- Retrieved Documents ---")
    for i, doc in enumerate(docs):
        print(f"[Doc {i + 1}]:")
        print(doc.page_content)
        print("-" * 50)

    # Step 3: Format prompt
    context = "\n".join([doc.page_content for doc in docs])
    template = system_prompt + "\n\nContext:\n{context}\n\nUser Query:\n{question}\n\nAnswer:"
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    # Step 4: Build RAG chain with retrieved context
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=None,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    # Step 5: Run QA
    result = qa_chain({"context": context, "question": user_input})

    print("\nLLM Response:", result)
    return result["result"]
