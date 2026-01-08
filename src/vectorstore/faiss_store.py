import faiss
import pickle
import os
import numpy as np

class FAISSStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, vectors, metadatas):
        self.index.add(np.array(vectors).astype("float32"))
        self.metadata.extend(metadatas)

    def search(self, q_vec, k=5):
        scores, idxs = self.index.search(q_vec.astype("float32"), k)
        return [self.metadata[i] for i in idxs[0]]

    def save(self, path):
        faiss.write_index(self.index, path + ".faiss")
        with open(path + ".meta.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls, path):
        index = faiss.read_index(path + ".faiss")
        with open(path + ".meta.pkl", "rb") as f:
            metadata = pickle.load(f)

        store = cls(index.d)
        store.index = index
        store.metadata = metadata
        return store
