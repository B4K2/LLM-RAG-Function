import chromadb
from sentence_transformers import SentenceTransformer
from function_registry import FUNCTION_METADATA

# Initialize vector DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="functions")

# Load sentence embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Store function descriptions in vector DB
for func_name, details in FUNCTION_METADATA.items():
    embedding = embedder.encode(details["description"]).tolist()
    collection.add(ids=[func_name], embeddings=[embedding])

def retrieve_best_function(prompt):
    """Retrieve the best function match dynamically using embeddings."""
    
    query_embedding = embedder.encode(prompt).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=1)

    return results["ids"][0][0] if results["ids"] else None
