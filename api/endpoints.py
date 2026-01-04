import time
from fastapi import APIRouter, HTTPException

from models import (QuestionRequest, QuestionResponse, DocumentRequest, DocumentResponse, StatusResponse)


class RagEndpoints:
    """Handler untuk semua RAG API endpoints"""
    
    def __init__(self, document_store, rag_workflow):
        self.document_store = document_store
        self.rag_workflow = rag_workflow
        self.router = self._create_router()
    
    def _create_router(self):
        """API routes"""
        router = APIRouter()
        
        router.add_api_route("/ask", self.ask_question, methods=["POST"])
        router.add_api_route("/add", self.add_document, methods=["POST"])
        router.add_api_route("/status", self.status, methods=["GET"])
        
        return router
    
    def ask_question(self, req: QuestionRequest) -> QuestionResponse:
        """function untuk memberikan pertanyaan dan dapatkan jawaban dari sistem RAG"""
        start = time.time()
        
        try:
            result = self.rag_workflow.ask(req.question)
            
            return QuestionResponse(
                question=req.question,
                answer=result["answer"],
                context_used=result.get("context", []),
                latency_sec=round(time.time() - start, 3)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def add_document(self, req: DocumentRequest) -> DocumentResponse:
        """function untuk menambahkan dokumen baru ke penyimpanan"""
        try:
            doc_id = self.document_store.add_document(req.text)
            return DocumentResponse(id=doc_id, status="added")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def status(self) -> StatusResponse:
        """function untuk cek system status"""
        store_status = self.document_store.get_status()
        
        return StatusResponse(
            qdrant_ready=store_status["qdrant_ready"],
            in_memory_docs_count=store_status["in_memory_docs_count"],
            graph_ready=self.rag_workflow.chain is not None
        )