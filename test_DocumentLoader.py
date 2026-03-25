from document_loader import DocumentLoader

def test_webpage():
    loader = DocumentLoader()
    docs = loader.load_webpage("https://www.uts.edu.au/about/faculties/engineering-and-information-technology/computer-science/research")
    print(f"Loaded {len(docs)} chunks from webpage")
    print(docs[0].page_content[:300])

def test_pdf():
    loader = DocumentLoader()
    docs = loader.load_pdf("sample.pdf")  # replace with a real PDF path
    print(f"Loaded {len(docs)} chunks from PDF")
    print(docs[0].page_content[:300])

if __name__ == "__main__":
    test_webpage()
    # test_pdf()  # uncomment when you have a PDF
