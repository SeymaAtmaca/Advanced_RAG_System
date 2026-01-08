import os
from src.ingestion.pdf_loader import load_pdf
from src.chunking.chunking import chunk_documents
from src.embedding.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore
from src.rag.pipeline import rag_pipeline
from src.llm.ollama import OllamaLLM


class RAGController:
    def __init__(self):
        self.embedder = Embedder("paraphrase-multilingual-mpnet-base-v2")
        self.llm = OllamaLLM(model="mistral")
        self.store = None
        self.chunks = None

    def load_pdf(self, pdf_path: str):
        """
        PDF seçildiğinde çağrılır.
        FAISS index burada oluşturulur.
        """
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # PDF_DIR = os.path.join(BASE_DIR, "pdfs")

        # pdf_path = os.path.join(PDF_DIR, "InceMemed2.pdf")

        if not os.path.exists(pdf_path):
            return False, "PDF bulunamadı"

        docs = load_pdf(pdf_path)
        if not docs:
            return False, "PDF okunamadı veya boş"

        chunks = chunk_documents(docs)
        if not chunks:
            return False, "Chunk oluşturulamadı"

        # ⬅️ KRİTİK: text + chunk beraber filtreleniyor
        valid_chunks = [c for c in chunks if c["text"].strip()]
        texts = [c["text"] for c in valid_chunks]

        vectors = self.embedder.encode(texts)
        if len(vectors) == 0:
            return False, "Embedding üretilemedi"

        self.store = FAISSStore(dim=len(vectors[0]))
        self.store.add(vectors, valid_chunks)
        self.chunks = valid_chunks

        return True, f"{len(valid_chunks)} parça indexlendi"

    def ask(self, question: str):
        """
        UI chat alanından çağrılır
        """
        if self.store is None:
            return "Önce bir PDF yükleyin.", []

        answer, pages = rag_pipeline(
            query=question,
            embedder=self.embedder,
            store=self.store,
            llm=self.llm
        )

        return answer, pages
    
    def _build_faiss(self, vectors, chunks):
        store = FAISSStore(dim=len(vectors[0]))
        store.add(vectors, chunks)
        return store

