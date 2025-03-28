from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from vector_db import retrieve_best_function  # Import Pinecone-based function retrieval
from param_extractor import extract_parameters
from code_generator import generate_code
from session_memory import (
    store_chat_session,
    retrieve_chat_history,
    get_or_create_session,
    get_db  # Dependency to get DB session
)

app = FastAPI()

class QueryModel(BaseModel):
    prompt: str

@app.post("/execute")
async def execute_function(query: QueryModel, request: Request, db: Session = Depends(get_db)):
    try:
        prompt = query.prompt
        user_ip = request.client.host  

        # Get or create session ID for user
        session_id = get_or_create_session(user_ip, db)  
        chat_history = retrieve_chat_history(session_id, db)

        # Use Pinecone-based function retrieval
        function_name = retrieve_best_function(prompt)

        # Handle vague prompts based on chat history
        if not function_name and chat_history:
            last_function = chat_history[-1]["function"]
            vague_phrases = ["do it again", "repeat", "what about", "other components", "more info"]
            if any(phrase in prompt.lower() for phrase in vague_phrases):
                function_name = last_function

        if function_name:
            params = extract_parameters(prompt, function_name, chat_history)
            code_snippet = generate_code(function_name, params)

            # Store chat session
            store_chat_session(session_id, prompt, function_name, params, db)

            return {"function": function_name, "generated_code": code_snippet}

        return JSONResponse(status_code=400, content={"error": "No matching function found"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
