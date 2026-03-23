from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document #Had to change this line from before
import os
from typing import List, Union


class DocumentLoader:
    """
    Handles loading and chunking of documents from URLs and PDFs.
    Produces clean, consistent LangChain Document objects for RAG pipelines.
    """

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """Load and chunk a PDF file."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        return self.splitter.split_documents(pages)

    def load_webpage(self, url: str) -> List[Document]:
        """Load and chunk a webpage."""
        loader = WebBaseLoader(url)
        docs = loader.load()
        return self.splitter.split_documents(docs)

    def load_multiple(self, sources: List[Union[str, dict]]) -> List[Document]:
        """
        Load multiple sources.
        Each source can be:
        - a PDF path (string ending in .pdf)
        - a URL (string starting with http)
        - a dict with custom metadata
        """
        all_docs = []

        for src in sources:
            if isinstance(src, str):
                if src.endswith(".pdf"):
                    all_docs.extend(self.load_pdf(src))
                elif src.startswith("http"):
                    all_docs.extend(self.load_webpage(src))
                else:
                    print(f"Skipping unknown source type: {src}")

            elif isinstance(src, dict):
                if src.get("type") == "pdf":
                    docs = self.load_pdf(src["path"])
                    for d in docs:
                        d.metadata.update(src.get("metadata", {}))
                    all_docs.extend(docs)

                elif src.get("type") == "url":
                    docs = self.load_webpage(src["url"])
                    for d in docs:
                        d.metadata.update(src.get("metadata", {}))
                    all_docs.extend(docs)

        return all_docs 