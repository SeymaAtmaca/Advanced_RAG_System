from src.rag.context_packer import pack_context

def rag_pipeline(query, embedder, store, llm, memory):
    q_vec = embedder.encode([query])[0]

    raw = store.search(q_vec.reshape(1, -1), k=20)
    packed = pack_context(q_vec, raw)

    context = "\n\n".join([c["text"] for c in packed])

    prompt = f"""
You are a precise document-based assistant.

Conversation history:
{memory.build()}

Context (use ONLY this):
{context}

Question:
{query}

Rules:
- Answer strictly from context
- If information is missing, say "Not found in document"
- Be concise and factual
"""

    answer = llm.generate(prompt)
    memory.add(query, answer)

    return answer, []
