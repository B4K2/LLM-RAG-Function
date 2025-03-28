# FastAPI AI-Powered Backend

## Overview
This FastAPI-based project enables AI-powered automation, system monitoring, and web automation tasks. It integrates NLP, vector databases, and cloud storage to process user queries dynamically. 

Key features include:
- **Intent Detection & Parameter Extraction**
- **AI-Powered Code Generation**
- **System Monitoring & Web Automation**
- **Database Integration (PostgreSQL & Pinecone for Vector Search)**
- **FastAPI-based API for easy integration**

---

## Installation
### Prerequisites
- Python 3.9+
- PostgreSQL (Configured on AWS)
- Pinecone API Key (For vector search functionality)
- Docker (Optional, currently facing optimization challenges)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables:
   - Create a `.env` file and configure credentials for PostgreSQL, Pinecone, and other required services.
   
4. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

## API Usage
### Example Requests & Responses
#### 1. **CPU Temperature Retrieval**
**Request:**
```json
{"prompt": "give me temp of cpu"}
```
**Response:**
```json
{
    "function": "get_system_info",
    "generated_code": "import psutil\n\ndef get_system_info(resource_type):\n    resource_mapping = {\n        \"cpu\": psutil.cpu_percent(interval=1),\n        \"ram\": psutil.virtual_memory().percent,\n        \"disk\": psutil.disk_usage('/').percent\n    }\n    return resource_mapping.get(resource_type, \"Invalid resource requested.\")\n\nif __name__ == \"__main__\":\n    print(get_system_info(\"cpu\"))"
}
```

#### 2. **Open Google Chrome**
**Request:**
```json
{"prompt": "open google chrome"}
```
**Response:**
```json
{
    "function": "web_automation",
    "generated_code": "from selenium import webdriver\nfrom selenium.webdriver.chrome.service import Service\nfrom webdriver_manager.chrome import ChromeDriverManager\n\ndef open_website(url):\n    service = Service(ChromeDriverManager().install())\n    driver = webdriver.Chrome(service=service)\n    driver.get(url)\n\nif __name__ == \"__main__\":\n    open_website(\"https://google\")"
}
```

#### 3. **Run a Shell Command**
**Request:**
```json
{"prompt": "run this command 'python run.py'"}
```
**Response:**
```json
{
    "function": "run_command",
    "generated_code": "import subprocess\n\ndef run_command(command):\n    try:\n        result = subprocess.run(command, shell=True, capture_output=True, text=True)\n        print(result.stdout)\n    except Exception as e:\n        print(f\"Error running command: {e}\")\n\nif __name__ == \"__main__\":\n    run_command(\"python run.py\")"
}
```

---

## Database & Vector Search
- **PostgreSQL (AWS Hosted)**: Stores structured data, including user sessions and query logs.
- **Pinecone Vector Search**: Enables efficient similarity search for NLP-powered features.

---

## Current Challenges & Optimizations
### 1. **Docker Image Size**
- The Docker container currently exceeds **12GB**, likely due to unnecessary dependencies or CUDA-related installations.
- Working on optimizing the Dockerfile to **reduce size** while maintaining functionality.

### 2. **AWS Deployment**
- AWS setup for PostgreSQL & Pinecone is functioning well, but deploying the entire FastAPI service efficiently while **minimizing cloud costs** is still in progress.
- Looking into **serverless options** (Lambda, Fargate) to keep resources off when not in use.

---

## Screenshot
![Alt text](https://github.com/B4K2/LLM-RAG-Function/blob/main/Screenshot%202025-03-28%20232351.png)

---

## Future Improvements
- Enhance **Dockerfile** to reduce unnecessary installations.
- Implement **serverless architecture** for better AWS cost-efficiency.
- Improve **error handling & logging** for API responses.

---

### Contributors
- **Akshat Balyan**  
Feel free to contribute, open issues, and suggest improvements!
