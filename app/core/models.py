from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    id: str = Field(..., description="ID único do chunk")
    document_id: str = Field(..., description="Nome ou ID do documento de origem")
    content: str = Field(..., description="Conteúdo do texto do chunk")
    page_number: Optional[int] = Field(default=None, description="Número da página")
    score: Optional[float] = Field(default=None, description="Score de similaridade")


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks_created: int
    status: str = "success"
    message: str = "Documento processado e indexado com sucesso."


class Citation(BaseModel):
    document_id: str
    page_number: Optional[int] = None
    snippet: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Pergunta do usuário")
    top_k: Optional[int] = Field(default=None, description="Quantidade de chunks a recuperar")


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str
    environment: str
