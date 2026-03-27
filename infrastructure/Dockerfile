# 1. Use a lightweight, stable Python base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies
# curl is required for the HEALTHCHECK instruction below
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install (Layer caching)
# This prevents re-installing packages if only your code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project structure into /app
COPY . .

# 6. CRITICAL: Set PYTHONPATH
# This allows 'src.main' to find 'src.logic' regardless of the entry point
ENV PYTHONPATH=/app

# 7. Monitoring: Docker Healthcheck
# Checks every 30s if the /health endpoint is responding with a 200 OK
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 8. Entrypoint: Start the FastAPI server
# We point to src.main:app because your 'app' instance is inside src/main.py
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]