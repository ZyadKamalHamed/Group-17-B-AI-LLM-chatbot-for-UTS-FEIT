from document_loader import DocumentLoader
from vector_store import VectorStore

loader = DocumentLoader()
docs = loader.load_webpage("https://www.uts.edu.au/about/faculty-engineering-and-it")

vs = VectorStore(model_name="nomic-embed-text")
vs.build(docs)
vs.save()
