from fastapi import FastAPI

from services.embedding import Embedding
from storage.document_store import DocumentStore
from services.rag_system import RagSystem
from api.endpoints import RagEndpoints


def create_app() -> FastAPI:
    """Function untuk membuat dan mengkonfigurasi FastAPI app"""
    
    # Initialize services
    embedding_service = Embedding(vector_size=128)
    document_store = DocumentStore(embedding_service)
    rag_workflow = RagSystem(document_store)
    
    # Create API endpoints
    endpoints = RagEndpoints(document_store, rag_workflow)
    
    # Setup FastAPI
    app = FastAPI(title="Learning RAG Demo")
    app.include_router(endpoints.router)
    
    return app


# Create app instance
app = create_app()