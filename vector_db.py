import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from function_registry import FUNCTION_METADATA
from dotenv import load_dotenv
load_dotenv() 


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not found! Set PINECONE_API_KEY as an environment variable.")

pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "function-search"

if INDEX_NAME not in [index["name"] for index in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384, 
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def store_functions():
    vectors = []
    for func_name, details in FUNCTION_METADATA.items():
        embedding = embedder.encode(details["description"]).tolist()
        vectors.append({"id": func_name, "values": embedding})
    
    index.upsert(vectors=vectors)

def retrieve_best_function(prompt):
    query_embedding = embedder.encode(prompt).tolist()
    results = index.query(vector=query_embedding, top_k=1, include_metadata=True)

    if results["matches"]:
        return results["matches"][0]["id"]  
    return None  

if __name__ == "__main__":
    store_functions()
