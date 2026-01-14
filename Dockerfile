# 1. Use Python 3.11 Slim (Lightweight)
FROM python:3.11-slim

# 2. Set Working Directory
WORKDIR /app

# 3. Install System Dependencies (Needed for Scikit-Learn/Pandas build)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the Application Code
COPY . .

# 6. Expose Ports (8000 for API, 8501 for UI)
EXPOSE 8000
EXPOSE 8501

# 7. Default Command (Starts the API)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
