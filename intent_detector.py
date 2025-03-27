from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

INTENT_CATEGORIES = {
    "open_application": "Launch a desktop application like Spotify, VLC, or Calculator.",
    "run_command": "Execute a shell command like 'ping google.com' or 'ls -la'.",
    "get_system_info": "Retrieve system stats like CPU, RAM, or disk usage.",
    "web_automation": "Automate a web browser to open websites, search queries, or interact with pages."
}

def detect_intent(prompt):
    """Use NLP to determine the correct function intent."""
    candidate_labels = list(INTENT_CATEGORIES.keys())
    result = classifier(prompt, candidate_labels)

    best_intent = result["labels"][0]

    web_keywords = ["open website", "search on google", "browse", "go to", "visit"]
    if any(word in prompt.lower() for word in web_keywords):
        return "web_automation"

    return best_intent
