FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn flask cloudflare requests
CMD ["python", "pond.py", "--server", "--a13", "--host", "0.0.0.0", "--port", "8080"]
