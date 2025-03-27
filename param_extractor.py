import re
import spacy

nlp = spacy.load("en_core_web_sm")

# List of known applications
COMMON_APPS = ["spotify", "vlc", "chrome", "firefox", "calculator", "notepad", "discord", "zoom"]

# List of websites for web automation
COMMON_WEBSITES = ["google", "youtube", "wikipedia", "twitter", "facebook", "github", "amazon"]

def extract_parameters(prompt, function_name):
    """Extract necessary parameters dynamically from the user prompt."""
    
    doc = nlp(prompt)
    extracted_param = None

    if function_name == "open_application":
        # Step 1: Use NER to detect application names
        extracted_param = next((ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]), None)

        # Step 2: Check known app list
        if not extracted_param:
            for app in COMMON_APPS:
                if app in prompt.lower():
                    extracted_param = app
                    break

        # Step 3: Regex fallback for applications
        if not extracted_param:
            match = re.search(r'(open|play|start|launch)\s+([a-zA-Z0-9-_]+)', prompt, re.IGNORECASE)
            if match:
                extracted_param = match.group(2).lower()

    elif function_name == "get_system_info":
        match = re.search(r'(cpu|ram|disk|memory|gpu)', prompt, re.IGNORECASE)
        extracted_param = match.group(1) if match else "cpu"

    elif function_name == "run_command":
        extracted_param = prompt.replace("run command", "").strip()

    elif function_name == "web_automation":
        # Extract website name
        extracted_website = None
        for site in COMMON_WEBSITES:
            if site in prompt.lower():
                extracted_website = site
                break
        
        # Extract search query if present
        search_match = re.search(r'(search for|look up|find)\s+(.+?)\s+(on|in)\s+(\w+)', prompt, re.IGNORECASE)
        if search_match:
            extracted_query = search_match.group(2).strip()
            extracted_website = search_match.group(4).strip()
            return [extracted_website, extracted_query]
        
        return [extracted_website] if extracted_website else ["google.com"]

    return [extracted_param] if extracted_param else ["unknown_param"]
