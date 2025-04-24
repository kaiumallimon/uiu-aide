from langchain.chains import RetrievalQA
from langchain.vectorstores import Weaviate
from apps.llm.gemini import llm, embedding_model
from config.supabase.supabase_client import supabase
from config.weaviate.weaviate_client import client as weaviate_client

def chat_with_agent(agent_id, user_question):
    # 1. Load agent config
    agent_data = supabase.table("agents").select("*").eq("id", agent_id).single().execute().data
    prompt_template = agent_data["prompt_template"]
    namespace = agent_data["vector_namespace"]

    # 2. Connect to Weaviate vectorstore
    vectorstore = Weaviate(
        client=weaviate_client,
        index_name="AgentDoc",
        embedding=embedding_model,
        tenant=namespace
    )

    # 3. Use RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

    return qa_chain.run(user_question)
