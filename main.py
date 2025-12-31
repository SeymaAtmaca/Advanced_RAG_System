from src.ingestion.pdf_loader import load_pdf
from src.chunking.chunking import chunk_documents
from src.embedding.embedder import Embedder 
from src.vectorstore.faiss_store import FAISSStore 
from src.rag.pipeline import rag_pipeline
from src.llm import openai
from src.llm import ollama

#Load pdf 
docs = load_pdf("InceMemed2.pdf")

chunks = chunk_documents(docs) 

embedder = Embedder("paraphrase-multilingual-mpnet-base-v2")
texts = [c["text"] for c in chunks]
vectors = embedder.encode(texts)
# llm = openai.OpenAI()

llm = ollama.OllamaLLM(model = "mistral")
store = FAISSStore(dim=len(vectors[0]))
store.add(vectors, chunks)

answer, pages = rag_pipeline(
    "dokümanın özetini ver", 
    embedder,
    store,
    llm
)

print("answer: ", answer)
print("sayfalar: ", pages)