import os
from src.ingestion.pdf_loader import load_pdf
from src.chunking.chunking import chunk_documents
from src.embedding.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore
from src.rag.pipeline import rag_pipeline
from src.llm.ollama import OllamaLLM
from src.rag.memory import ChatMemory


class RAGController:
    def __init__(self):
        self.embedder = Embedder("paraphrase-multilingual-mpnet-base-v2")
        self.llm = OllamaLLM(model="mistral")
        self.store = None
        self.chunks = None
        self.memory = ChatMemory(max_turns=5)

    def load_pdf(self, pdf_path, progress_callback=None):
        docs = load_pdf(pdf_path)
        chunks = chunk_documents(docs)

        valid_chunks = [c for c in chunks if c["text"].strip()]
        texts = [c["text"] for c in valid_chunks]

        vectors = self.embedder.encode(
            texts,
            batch_size=32,
            progress_callback=progress_callback
        )

        self.store = FAISSStore(dim=len(vectors[0]))
        self.store.add(vectors, valid_chunks)
        self.chunks = valid_chunks
        self.memory.clear()

        return True, f"{len(valid_chunks)} chunks indexed"


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
            llm=self.llm,
            memory = self.memory
        )

        return answer, pages
    
    def _build_faiss(self, vectors, chunks):
        store = FAISSStore(dim=len(vectors[0]))
        store.add(vectors, chunks)
        return store

