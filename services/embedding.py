import random


class Embedding:
    """Service untuk generate embeddings dari teks"""
    
    def __init__(self, vector_size=128):
        self.vector_size = vector_size
    
    def embed(self, text: str) -> list[float]:
        """Generate fake embedding yang deterministik berdasarkan input text"""
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)]