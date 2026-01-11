import faiss
import pickle
import numpy as np

class FAISSStore:
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.vectors = []
        self.chunks = []

    def add(self, vectors, chunks):
        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)
        self.vectors.extend(vectors)
        self.chunks.extend(chunks)

    def search(self, query_vec, k=10):
        query_vec = np.array(query_vec).astype("float32")
        D, I = self.index.search(query_vec, k)

        results = []
        for idx in I[0]:
            if idx == -1:
                continue

            results.append({
                "text": self.chunks[idx]["text"],
                "page": self.chunks[idx]["page"],
                "vector": self.vectors[idx]
            })

        return results

    def save(self, path):
        faiss.write_index(self.index, path + ".faiss")
        with open(path + ".pkl", "wb") as f:
            pickle.dump({
                "vectors": self.vectors,
                "chunks": self.chunks
            }, f)

    @classmethod
    def load(cls, path):
        index = faiss.read_index(path + ".faiss")
        with open(path + ".pkl", "rb") as f:
            data = pickle.load(f)

        store = cls(index.d)
        store.index = index
        store.vectors = data["vectors"]
        store.chunks = data["chunks"]

        return store
