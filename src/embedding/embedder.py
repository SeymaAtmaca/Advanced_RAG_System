from sentence_transformers import SentenceTransformer
import math
import numpy as np

class Embedder:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=32, progress_callback=None):
        vectors = []
        total = len(texts)
        total_batches = math.ceil(total / batch_size)

        for i in range(0, total, batch_size):
            batch = texts[i:i+batch_size]
            emb = self.model.encode(batch, show_progress_bar=False)
            emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
            vectors.extend(emb)

            if progress_callback:
                current_batch = (i // batch_size) + 1
                percent = int((current_batch / total_batches) * 100)
                progress_callback(percent)

        return np.array(vectors)
