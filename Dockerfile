# Use the official Python image as base
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the pre-converted GGUF model into the Docker image
COPY ./model_cache_gguf/llama-3.1-8b.gguf ./model_cache_gguf/llama-3.1-8b.gguf

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["python", "llama.py"]
