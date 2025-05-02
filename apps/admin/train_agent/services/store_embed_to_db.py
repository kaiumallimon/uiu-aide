from pinecone import Pinecone
from config import settings


def save_training_data_to_pinecone_db(agent_id: str, pinecone_data: list):
    # initialize pinecone
    pinecone = Pinecone(
        api_key = settings.PINECONE_API_KEY
    )

    index_name = "uiu-aide"

    if not pinecone.has_index(name=index_name):
        raise ValueError(f"Index {index_name} does not exist.")

    index = pinecone.Index(index_name)

    # Upsert the data into the Pinecone index
    try:
        index.upsert(vectors=pinecone_data)
        print(f"Successfully upserted {len(pinecone_data)} items into Pinecone index '{index_name}'.")
    except Exception as e:
        raise ValueError(f"Failed to upsert data into Pinecone: {e}")
