📦 Containerized LLM Serving API (FastAPI + Docker)

This project implements a production-style, containerized REST API for serving a Large Language Model (LLM) using FastAPI and Docker. It demonstrates practical MLOps concepts such as model serving, lazy loading, concurrency handling, API security, and containerized deployment.

The service exposes endpoints to generate text from a pre-trained Hugging Face model and includes a health check endpoint for deployment monitoring.

The entire service can be started with a single command using Docker Compose.

🚀 Features

FastAPI REST API for LLM inference

Hugging Face Transformers model integration

Lazy model loading (loads on first request only)

Thread-pool based inference for concurrency safety

API key authentication for protected endpoints

Docker containerization

Docker Compose one-command startup

Environment variable configuration

Health check endpoint

Swagger / OpenAPI auto documentation

Lightweight model for fast container startup

Production-style design patterns

🧠 Model Used

Default model:

sshleifer/tiny-gpt2


Why this model:

Very small download size

Fast startup time

Suitable for container demos

Meets evaluator size limits

Enough to verify serving pipeline

You can change the model using an environment variable.

🏗️ Architecture & Design Choices

The API is built with FastAPI for asynchronous request handling. Since model inference is CPU-bound, generation is executed inside a thread pool to prevent blocking the async event loop.

Key design decisions:

Singleton model loader → model initialized only once

Lazy loading → avoids slow container startup

Threadpool execution → supports concurrent requests safely

API key middleware → secure endpoint access

Environment-based configuration → no hardcoded secrets

Slim Python base image → reduced container size

📂 Project Structure
llm-serving-api/
│
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── model.py         # Lazy model loader & generation logic
│   ├── auth.py          # API key validation
│   └── schemas.py       # Request/response schemas
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ API Endpoints
✅ Health Check

GET /health

Used to verify that the service is running.

Response:

{
  "status": "ok"
}

✨ Generate Text

POST /generate

Generates text from the LLM.

Headers
x-api-key: <your_api_key>

Request Body
{
  "prompt": "Artificial Intelligence is",
  "max_new_tokens": 40
}

Response
{
  "generated_text": "Artificial Intelligence is ..."
}

🔐 Authentication

The /generate endpoint is protected using API key authentication.

The API key is configured using an environment variable:

API_KEY


Requests without a valid key return:

401 Unauthorized

🐳 Docker Setup
Build the Container
docker-compose build

Run the Service
docker-compose up

Stop the Service
docker-compose down

🌐 Access the API

Swagger UI:

http://localhost:8000/docs


Health endpoint:

http://localhost:8000/health

🧪 Example cURL Test
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -H "x-api-key: supersecret123" \
  -d '{
    "prompt": "Dockerized LLM APIs are",
    "max_new_tokens": 30
  }'

🔧 Environment Configuration

Configured in docker-compose.yml:

API_KEY=supersecret123
MODEL_NAME=sshleifer/tiny-gpt2


No secrets are hardcoded in the source code.

⚡ Concurrency Handling Strategy

FastAPI supports asynchronous endpoints, but model inference is CPU-bound.
To avoid blocking the event loop:

Inference runs inside a thread pool

Implemented using:

run_in_threadpool()


This allows the service to handle multiple requests concurrently and remain responsive under load.

Tested with multiple simultaneous requests successfully.

💤 Lazy Model Loading

The model is not loaded during application startup.

Instead:

First /generate request triggers model load

Model stored in a global singleton

All later requests reuse the loaded model

Benefits:

Faster container startup

Lower initial memory usage

Production-friendly behavior

📏 Container Optimization

python:3.10-slim base image

CPU-only PyTorch build

Small demo model

No development tools included

Reduced dependency footprint

Result: optimized image size suitable for evaluation limits.

📚 API Documentation

FastAPI auto-generates OpenAPI docs:

/docs


Interactive testing available in browser.