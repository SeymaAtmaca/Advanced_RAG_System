import numpy as np

def pack_context(query_vec, retrieved_chunks, max_tokens=1800):
    """
    Reorders and filters FAISS results so the LLM sees only the most
    semantically useful chunks in the correct order.
    """

    # Cosine similarity ordering
    for c in retrieved_chunks:
        c["score"] = float(np.dot(query_vec, c["vector"]))

    # highest relevance first
    ranked = sorted(retrieved_chunks, key=lambda x: x["score"], reverse=True)

    packed = []
    token_count = 0

    for c in ranked:
        tokens = len(c["text"].split())

        if token_count + tokens > max_tokens:
            break

        packed.append(c)
        token_count += tokens

    return packed
