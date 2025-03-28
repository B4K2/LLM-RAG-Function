# Use an official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies without installing torch
RUN pip install --no-deps sentence-transformers==3.4.1
RUN pip install -r requirements.txt && pip uninstall -y torch

# Copy the rest of the application
COPY . .

# Expose port and set entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
