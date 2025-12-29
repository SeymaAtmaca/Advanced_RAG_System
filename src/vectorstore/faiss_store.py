import faiss 
import numpy as np 

class FAISSStore:
    def __init__(self, dim):
        """
        dim: enbedding vector dimension
        """
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vectors, metadatas):
        """
        vectors : List[np.array] = embedding vectors 
        metadata: List[dict] = chunk info (text, page)
        """
        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadatas) 

    def search(self, query_vector, k= 5):
        """
        query_vector = np.array shape (1, dim)
        returns: List[dict] = top-k chunk metadata
        """
        query_vector = np.array(query_vector).astype("float32")
        distances, indices = self.index.search(query_vector, k)

        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results