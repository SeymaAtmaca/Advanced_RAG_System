from src.rag.prompt import build_prompt


def rag_pipeline(query, embedder, store, llm):
    q_vec = embedder.encode([query])
    retrieved = store.search(q_vec, k=5)

    context = ""
    pages = set()

    for item in retrieved:
        context += item["text"] + "\n"
        pages.add(item["page"])

    prompt = build_prompt(context, query)
    answer = llm.generate(prompt)

    return answer, sorted(pages)