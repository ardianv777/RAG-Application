from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


class DocumentStore:
    """Simple document store with Qdrant integration and in-memory fallback"""
    
    def __init__(self, embedding_service, qdrant_url="http://localhost:6333"):
        self.embedding_service = embedding_service
        self.docs_memory = []
        self.using_qdrant = False
        
        # Try to connect to Qdrant
        try:
            self.qdrant = QdrantClient(qdrant_url)
            self.qdrant.recreate_collection(
                collection_name="demo_collection",
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.using_qdrant = True
            print("✅ Qdrant connected")
        except Exception as e:
            print(f"⚠️ Qdrant not available. Using in-memory fallback.")
            self.using_qdrant = False
    
    def add_document(self, text: str) -> int:
        """Add a new document to the store"""
        embedding = self.embedding_service.fake_embed(text)
        doc_id = len(self.docs_memory)
        
        if self.using_qdrant:
            self.qdrant.upsert(
                collection_name="demo_collection",
                points=[PointStruct(
                    id=doc_id, 
                    vector=embedding, 
                    payload={"text": text}
                )]
            )
        else:
            self.docs_memory.append(text)
        
        return doc_id
    
    def search_documents(self, query: str, limit=2) -> list[str]:
        """Search for documents relevant to the query"""
        query_embedding = self.embedding_service.fake_embed(query)
        results = []
        
        if self.using_qdrant:
            hits = self.qdrant.search(
                collection_name="demo_collection",
                query_vector=query_embedding,
                limit=limit
            )
            results = [hit.payload["text"] for hit in hits]
        else:
            # Simple substring match in memory
            for doc in self.docs_memory:
                if query.lower() in doc.lower():
                    results.append(doc)
            
            # If nothing is found, take the first document
            if not results and self.docs_memory:
                results = [self.docs_memory[0]]
        
        return results
    
    def get_status(self) -> dict:
        """Return status of the document store"""
        return {
            "qdrant_ready": self.using_qdrant,
            "in_memory_docs_count": len(self.docs_memory)
        }