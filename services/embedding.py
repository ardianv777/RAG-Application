import random


class Embedding:
    """embedding service sederhana yang menghasilkan embedding palsu"""
    
    def __init__(self, vector_size=128):
        self.vector_size = vector_size
    
    def fake_embed(self, text: str) -> list[float]:
        """Function untuk menghasilkan embedding palsu untuk teks yang diberikan"""
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)] # Small vector for demo