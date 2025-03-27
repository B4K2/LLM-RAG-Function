import json

# In-memory dictionary for session storage (Resets when server restarts)
session_data = {}

def get_or_create_session(user_ip):
    """Check if user has an existing session, otherwise create a new one."""
    if user_ip not in session_data:
        session_data[user_ip] = []
    return user_ip  # Use user_ip as session_id

def store_chat_session(session_id, user_prompt, function_name, params):
    """Store user interactions in session memory."""
    session_data[session_id].append({"prompt": user_prompt, "function": function_name, "params": params})

def retrieve_chat_history(session_id, last_n=5):
    """Retrieve the last N interactions from session memory."""
    return session_data.get(session_id, [])[-last_n:]
