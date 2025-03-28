import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from function_registry import FUNCTION_METADATA
from dotenv import load_dotenv

load_dotenv()

# Load Pinecone API key from environment variable
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not found! Set PINECONE_API_KEY as an environment variable.")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name
INDEX_NAME = "function-search"

# Check existing indexes correctly
existing_indexes = [index.name for index in pc.list_indexes()]

# Create index if it doesn't exist
if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # SentenceTransformer("all-MiniLM-L6-v2") output dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the created index
index = pc.Index(INDEX_NAME)

# Load sentence embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Store function descriptions in Pinecone
def store_functions():
    vectors = []
    for func_name, details in FUNCTION_METADATA.items():
        embedding = embedder.encode(details["description"]).tolist()
        vectors.append((func_name, embedding, {}))  # Correct tuple format (id, values, metadata)
    
    # Upsert vectors in Pinecone
    index.upsert(vectors=vectors)
    print(f"✅ Stored {len(vectors)} function descriptions in Pinecone.")

# Retrieve the best function match based on a query
def retrieve_best_function(prompt):
    query_embedding = embedder.encode(prompt).tolist()
    results = index.query(vector=query_embedding, top_k=1, include_metadata=True)

    if "matches" in results and results["matches"]:
        return results["matches"][0]["id"]  # Return the best matching function name
    return None  # No match found

# Store functions in Pinecone when script runs
if __name__ == "__main__":
    store_functions()
