from fastapi import FastAPI, Depends
from fastapi.concurrency import run_in_threadpool
from app.schemas import GenerateRequest, GenerateResponse
from app.model import generate_text
from app.auth import verify_api_key

app = FastAPI(title="LLM Serving API")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(
    req: GenerateRequest,
    _: str = Depends(verify_api_key)
):
    text = await run_in_threadpool(
        generate_text,
        req.prompt,
        req.max_new_tokens
    )

    return {"generated_text": text}
