from jinja2 import Template

TEMPLATES = {
    "open_application": Template(
        """import subprocess

def open_application(app_name):
    try:
        subprocess.Popen(app_name, shell=True)
        print(f"Opened application: {app_name}")
    except Exception as e:
        print(f"Error opening application: {e}")

if __name__ == "__main__":
    open_application("{{ param1 }}")
"""
    ),
    
    "run_command": Template(
        """import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error running command: {e}")

if __name__ == "__main__":
    run_command("{{ param1 }}")
"""
    ),
    
    "get_system_info": Template(
        """import psutil

def get_system_info(resource_type):
    resource_mapping = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    return resource_mapping.get(resource_type, "Invalid resource requested.")

if __name__ == "__main__":
    print(get_system_info("{{ param1 }}"))
"""
    ),

    "calculate_expression": Template(
        """import ast

def calculate_expression(expression):
    try:
        result = ast.literal_eval(expression) 
        print(f"Result: {result}")
    except (ValueError, SyntaxError):
        print("Invalid expression")

if __name__ == "__main__":
    calculate_expression("{{ param1 }}")
"""
    ),

    "web_automation": Template(
        """from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open_website(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

if __name__ == "__main__":
    open_website("https://{{ param1 }}")
"""
    )
}
