from sentence_transformers import SentenceTransformer 

class Embedder:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, normalize_embeddings=True):
        return self.model.encode(
            texts, 
            normalize_embeddings = normalize_embeddings,
            show_progress_bar = True
        )
    