from document_loader import DocumentLoader
from vector_store import VectorStore
from data.URLS import Web_links

loader = DocumentLoader()
vs = VectorStore()
docs = loader.load_multiple(list(Web_links.values()))
print(f"Loaded {len(docs)} chunks from {len(Web_links)} pages")

vs.build(docs)