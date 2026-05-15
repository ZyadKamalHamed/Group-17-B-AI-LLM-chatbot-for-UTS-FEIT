from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List
import os


class VectorStore:
    def __init__(self, model_name="nomic-embed-text", persist_dir="chroma_db"):
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.persist_dir = persist_dir
        self.store = None

    def build(self, docs: List[Document]):
        self.store = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        return self.store

    def load(self):
        self.store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir
        )
        return self.store

    def as_retriever(self, k=4):
        return self.store.as_retriever(search_kwargs={"k": k})