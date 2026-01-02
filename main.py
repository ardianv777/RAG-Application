import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.embedding import Embedding
from storage.document_store import DocumentStore
from services.rag_system import RagSystem


# Initialize services
embedding_service = Embedding(vector_size=128)
document_store = DocumentStore(embedding_service)
rag_workflow = RagSystem(document_store)

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
    """Ask a question dan get answer dari RAG system"""
    start = time.time()
    
    try:
        result = rag_workflow.ask(req.question)
        
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
    """Add dokumen baru ke system"""
    try:
        doc_id = document_store.add_document(req.text)
        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    """Check system status"""
    store_status = document_store.get_status()
    
    return {
        **store_status,
        "graph_ready": rag_workflow.chain is not None
    }