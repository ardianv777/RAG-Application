from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request model for ask endpoint"""
    question: str


class DocumentRequest(BaseModel):
    """Request model for add document endpoint"""
    text: str


class QuestionResponse(BaseModel):
    """Response model for ask endpoint"""
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float


class DocumentResponse(BaseModel):
    """Response model for add document endpoint"""
    id: int
    status: str


class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool