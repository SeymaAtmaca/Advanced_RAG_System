from src.rag.prompt import build_prompt
from src.reranker.cross_encoder import CrossEncoderReranker
from src.rag.memory import ChatMemory

def rag_pipeline(query, embedder, store, llm):
    memory = ChatMemory(max_turns=5)
    q_vec = embedder.encode([query], normalize_embeddings=True)
    retrieved = store.search(q_vec, k=10)

    context = "\n".join([r["text"] for r in retrieved])
    pages = sorted({r["page"] for r in retrieved})

    prompt = f"""
Conversation:
{memory.build()}

Context:
{context}

Question:
{query}

Answer using ONLY the context. Cite pages.
"""

    answer = llm.generate(prompt)
    memory.add(query, answer)

    return answer, pages

