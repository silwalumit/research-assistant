FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
RUN mkdir -p data/chroma
COPY docs/ ./docs/


# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "src.cmd.main:app", "--host", "0.0.0.0", "--port", "8000"]

