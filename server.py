from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web_rag_pipeline import WebRAGPipeline
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise the Web‑RAG pipeline
pipeline = WebRAGPipeline()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Web‑RAG endpoint:
    1. Search the web
    2. Extract content
    3. Build context
    4. Generate grounded answer
    5. Return answer + sources
    """
    return pipeline.run(request.question)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
