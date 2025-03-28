import re
import spacy

nlp = None 

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")  
    return nlp

COMMON_APPS = ["spotify", "vlc", "chrome", "firefox", "calculator", "notepad", "discord", "zoom"]
COMMON_WEBSITES = ["google", "youtube", "wikipedia", "twitter", "facebook", "github", "amazon"]

def extract_parameters(prompt, function_name, chat_history=None):
    doc = get_nlp()(prompt)
    extracted_param = None

    if function_name == "open_application":
        extracted_param = next((ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]), None)

        if not extracted_param:
            for app in COMMON_APPS:
                if app in prompt.lower():
                    extracted_param = app
                    break

        if not extracted_param:
            match = re.search(r'(open|play|start|launch)\s+([a-zA-Z0-9-_]+)', prompt, re.IGNORECASE)
            if match:
                extracted_param = match.group(2).lower()

    elif function_name == "get_system_info":
        components = re.findall(r'(cpu|ram|disk|memory|gpu)', prompt, re.IGNORECASE)

        if not components and chat_history and len(chat_history) > 0:
            last_entry = chat_history[-1]
            last_param = last_entry["params"][0] if last_entry["params"] else "cpu"

            if "other" in prompt.lower() or "components" in prompt.lower():
                components = ["ram", "disk"] if last_param == "cpu" else ["cpu", "disk"]

        extracted_param = components if components else ["cpu"]

    elif function_name == "run_command":
        extracted_param = [prompt.replace("run command", "").strip()]  

    elif function_name == "web_automation":
        extracted_website = None
        for site in COMMON_WEBSITES:
            if site in prompt.lower():
                extracted_website = site
                break
        
        search_match = re.search(r'(search for|look up|find)\s+(.+?)\s+(on|in)\s+(\w+)', prompt, re.IGNORECASE)
        if search_match:
            extracted_query = search_match.group(2).strip()
            extracted_website = search_match.group(4).strip()
            return [extracted_website, extracted_query]  
        
        return [extracted_website] if isinstance(extracted_website, str) else ["google.com"]

    return [extracted_param] if isinstance(extracted_param, str) else extracted_param if extracted_param else ["unknown_param"]
