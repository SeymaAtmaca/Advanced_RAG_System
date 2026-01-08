from src.ingestion.pdf_loader import load_pdf
from src.chunking.chunking import chunk_documents
from src.embedding.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore
from src.rag.pipeline import rag_pipeline
from src.llm import ollama
import os


class RAGController:
    def __init__(self, pdf_dir="data"):
        self.pdf_dir = pdf_dir
        self.embedder = Embedder("paraphrase-multilingual-mpnet-base-v2")
        self.llm = ollama.OllamaLLM(model="mistral")
        self.store = None
        self._build_index()

    def _build_index(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        PDF_DIR = os.path.join(BASE_DIR, "data")

        pdf_path = os.path.join(PDF_DIR, "InceMemed2.pdf")

        docs = load_pdf(pdf_path)
        
        if not docs:
            raise RuntimeError("PDF yüklenemedi veya boş")

        chunks = chunk_documents(docs)

        if not chunks:
            raise RuntimeError("Chunk oluşturulamadı")

        texts = [c["text"] for c in chunks if c["text"].strip()]

        if not texts:
            raise RuntimeError("Embedding için text yok")

        vectors = self.embedder.encode(texts)

        if len(vectors) == 0:
            raise RuntimeError("Embedding sonucu boş")

        self.store = FAISSStore(dim=len(vectors[0]))
        self.store.add(vectors, chunks)


    def ask(self, question):
        answer, pages = rag_pipeline(
            question,
            self.embedder,
            self.store,
            self.llm
        )
        return answer, pages
