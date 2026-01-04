from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request model untuk ask endpoint"""
    question: str


class DocumentRequest(BaseModel):
    """Request model untuk add document endpoint"""
    text: str


class QuestionResponse(BaseModel):
    """Response model untuk ask endpoint"""
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float


class DocumentResponse(BaseModel):
    """Response model untuk add document endpoint"""
    id: int
    status: str


class StatusResponse(BaseModel):
    """Response model untuk status endpoint"""
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool