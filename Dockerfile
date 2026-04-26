# ============================================================
# Adaptive RAG - Dockerfile
# ============================================================
# Build the image:
#   docker build -t adaptive-rag .
#
# Run the container:
#   docker run -p 8000:8000 --env-file .env adaptive-rag
# ============================================================

# Use official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (so Docker caches this layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
