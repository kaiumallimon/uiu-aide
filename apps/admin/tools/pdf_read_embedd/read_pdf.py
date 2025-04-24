from langchain_google_genai import  GoogleGenerativeAIEmbeddings
from langchain.vectorstores import  Weaviate
from langchain.text_splitter import  RecursiveCharacterTextSplitter

from config.weaviate.weaviate_client import get_weaviate_client
from utils.extract_pdf_text import extract_pdf_text


# initialize Gemini embeddings
EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

# embedd and store pdf files
def embed_and_store_pdf_in_weaviate(pdf_path,namespace):
    text = extract_pdf_text(pdf_path)

    # Split the text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    documents = splitter.create_documents([text])

    client = get_weaviate_client()

    # Ensure class/schema exists
    class_name = namespace.replace("-", "_").capitalize()
    if not client.schema.contains(class_name):
        client.schema.create_class(
            {
                "class": class_name,
                "vectorIndexType": "hnsw",
                "vectorIndexConfig": {
                    "distance": "cosine",
                    "efConstruction": 128,
                    "maxConnections": 64,
                    "minConnections": 16,
                    "numNeighbors": 10
                },
                "properties": [
                    {
                        "name": "text",
                        "dataType": ["text"]
                    }
                ]
            }
        )

    # use langchain's weaviate wrapper to store the documents
    vectorstore = Weaviate(
        client=client,
        index_name=class_name,
        embedding_function=EMBEDDING_MODEL.embed_query,
        text_key="text",
        namespace=namespace
    )


    # Store the documents in Weaviate
    vectorstore.add_documents(documents)

    return class_name