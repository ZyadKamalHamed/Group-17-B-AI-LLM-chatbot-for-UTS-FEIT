from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.tools import DuckDuckGoSearchRun
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

search = DuckDuckGoSearchRun()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: ChatRequest):
    result = search.run(request.question)
    return {"answer": result, "sources": []}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
