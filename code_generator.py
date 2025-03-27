def generate_code(function_name, params):
    """Generate structured Python code dynamically."""

    function_templates = {
        "open_application": """import subprocess

def open_application(app_name):
    try:
        subprocess.Popen(app_name, shell=True)
        print(f"Opened application: {app_name}")
    except Exception as e:
        print(f"Error opening application: {e}")

if __name__ == "__main__":
    open_application("{param1}")
""",
        "run_command": """import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error running command: {e}")

if __name__ == "__main__":
    run_command("{param1}")
""",
        "get_system_info": """import psutil

def get_system_info(resource_type):
    resource_mapping = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    return resource_mapping.get(resource_type, "Invalid resource requested.")

if __name__ == "__main__":
    print(get_system_info("{param1}"))
""",
        "calculate_expression": """def calculate_expression(expression):
    try:
        result = eval(expression)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error calculating expression: {e}")

if __name__ == "__main__":
    calculate_expression("{param1}")
""",
        "web_automation": """from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def open_website(url):
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(url)
    print(f"Opened website: {url}")

if __name__ == "__main__":
    open_website("https://{param1}")
"""
    }

    return function_templates[function_name].replace("{param1}", params[0])
