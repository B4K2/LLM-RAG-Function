from fastapi import FastAPI, Request
from pydantic import BaseModel

from intent_detector import detect_intent
from param_extractor import extract_parameters
from code_generator import generate_code
from session_memory import store_chat_session, retrieve_chat_history, get_or_create_session

app = FastAPI()

class QueryModel(BaseModel):
    prompt: str

@app.post("/execute")
async def execute_function(query: QueryModel, request: Request):
    prompt = query.prompt

    # Get user IP for session tracking (acts as a session ID)
    user_ip = request.client.host  
    session_id = get_or_create_session(user_ip)  

    # Retrieve chat history (last 5 messages)
    chat_history = retrieve_chat_history(session_id)

    # Detect function intent from the current prompt
    function_name = detect_intent(prompt)

    # **Only use chat history if the new prompt is vague**
    if not function_name and chat_history:
        last_function = chat_history[-1]["function"]
        
        # Allow fallback ONLY if the prompt is a vague reference
        vague_phrases = ["do it again", "repeat", "same again", "one more time"]
        if any(phrase in prompt.lower() for phrase in vague_phrases):
            function_name = last_function

    if function_name:
        # Extract parameters dynamically
        params = extract_parameters(prompt, function_name)

        # Generate executable Python code
        code_snippet = generate_code(function_name, params)

        # Store the interaction in session memory
        store_chat_session(session_id, prompt, function_name, params)

        return {
            "function": function_name,
            "generated_code": code_snippet,
            "session_id": session_id
        }

    return {"error": "No matching function found"}
