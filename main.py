import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.embedding import Embedding
from storage.document_store import DocumentStore
from services.rag_system import RagSystem


# Initialize services
embedding = Embedding(vector_size=128)
document_store = DocumentStore(embedding)
rag_system = RagSystem(document_store)

# FastAPI app
app = FastAPI(title="Learning RAG Demo")


# Request models
class QuestionRequest(BaseModel):
    question: str


class DocumentRequest(BaseModel):
    text: str


# Endpoints
@app.post("/ask")
def ask_question(req: QuestionRequest):
    """Add a new document to the system"""
    start = time.time()
    
    try:
        result = rag_system.ask(req.question)
        
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add")
def add_document(req: DocumentRequest):
    """Add a new document to the system"""
    try:
        doc_id = document_store.add_document(req.text)
        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    """Get system status"""
    store_status = document_store.get_status()
    
    return {
        **store_status,
        "graph_ready": rag_system.chain is not None
    }