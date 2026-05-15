# UTS FEIT Chatbot

A chatbot for UTS Faculty of Engineering and IT students. It answers questions about courses, enrolment, important dates, policies, and campus life using UTS web pages.

## How it works

Streamlit frontend talks to a FastAPI backend. The backend runs a Web-RAG pipeline that searches with DuckDuckGo, filters results to trusted UTS domains, scrapes the pages, and asks a local LLM (via Ollama) to write the answer using only what was retrieved.

## Setup

### 1. Install Ollama

Download from [ollama.com](https://ollama.com) and start the server:

```
ollama serve
```

### 2. Pull the models

```
ollama pull llama3:8b
ollama pull nomic-embed-text
```

`llama3:8b` is used for the answers. `nomic-embed-text` is used for embedding the PDFs.

### 3. Install Python dependencies

```
pip install -r requirements.txt
```

## Running

Open two terminals.

Backend:

```
python server.py
```

Frontend:

```
streamlit run app.py
```

Then open the Streamlit URL it prints (http://localhost...).

## Project structure

- `app.py` — Streamlit UI
- `server.py` — FastAPI backend
- `web_rag_pipeline.py` — search, scrape, and answer logic
- `vector_store.py` — Chroma wrapper for the local PDFs
- `document_loader.py` — PDF and webpage loaders
- `data/` — PDFs to index
- `chroma_db/` — generated vector store (created on first run)
