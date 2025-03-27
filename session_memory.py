import json

session_data = {}

def get_or_create_session(user_ip):
    if user_ip not in session_data:
        session_data[user_ip] = []
    return user_ip 

def store_chat_session(session_id, user_prompt, function_name, params):
    session_data[session_id].append({"prompt": user_prompt, "function": function_name, "params": params})

def retrieve_chat_history(session_id, last_n=5):
    return session_data.get(session_id, [])[-last_n:]
