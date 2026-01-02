import random


class Embedding:
    """Simple embedding service that generates fake embeddings"""
    
    def __init__(self, vector_size=128):
        self.vector_size = vector_size
    
    def fake_embed(self, text: str) -> list[float]:
        """Generate a fake embedding for the given text"""
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)] # Small vector for demo