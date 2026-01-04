from src.rag.prompt import build_prompt
from src.reranker.cross_encoder import CrossEncoderReranker


def rag_pipeline(query, embedder, store, llm):
    q_vec = embedder.encode(texts = [query], normalize_embeddings=True)

    retrieved = store.search(q_vec, k=30)

    # If add ReRanker ro model, open this 2 lines
    # reranker = CrossEncoderReranker()
    # retrieved = reranker.rerank(query, retrieved, top_k=10)

    context = ""
    pages = set()

    for item in retrieved:
        context += item["text"] + "\n"
        pages.add(item["page"])

    prompt = build_prompt(context, query)
    answer = llm.generate(prompt)

    return answer, sorted(pages)
