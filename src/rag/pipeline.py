from src.rag.prompt import build_prompt
from src.reranker.cross_encoder import CrossEncoderReranker
from src.rag.memory import ChatMemory
from src.rag.context_packer import pack_context

def rag_pipeline(query, embedder, store, llm, memory):
    # memory = ChatMemory(max_turns=5)
    q_vec = embedder.encode([query])
    raw = store.search(q_vec, k=20)
    retrieved = pack_context(q_vec[0], raw)

    context = "\n\n".join([c["text"] for c in retrieved])
    pages = sorted({c["page"] for c in retrieved})


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

