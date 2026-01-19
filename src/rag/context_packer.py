import numpy as np

MAX_CHARS = 3500  # mistral için güvenli

def pack_context(query_vec, retrieved_chunks):
    for c in retrieved_chunks:
        c["score"] = float(np.dot(query_vec, c["vector"]))

    ranked = sorted(retrieved_chunks, key=lambda x: x["score"], reverse=True)

    packed = []
    total_len = 0

    for c in ranked:
        text = c["text"]
        if total_len + len(text) > MAX_CHARS:
            break
        packed.append(c)
        total_len += len(text)

    return packed
