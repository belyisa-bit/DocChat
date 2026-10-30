from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ==========================================
# Schemas de Documentos e Chunks
# ==========================================

class DocumentChunk(BaseModel):
    """Representa um pedaço (chunk) de texto extraído de um documento."""
    id: str = Field(..., description="ID único do chunk")
    document_id: str = Field(..., description="Nome ou ID do documento de origem")
    content: str = Field(..., description="Conteúdo do texto do chunk")
    page_number: Optional[int] = Field(default=None, description="Número da página (se aplicável)")
    score: Optional[float] = Field(default=None, description="Score de similaridade/relevância do retrieval")


class DocumentUploadResponse(BaseModel):
    """Resposta após ingestão/upload de um documento."""
    filename: str
    chunks_created: int
    status: str = "success"
    message: str = "Documento processado e indexado com sucesso."


# ==========================================
# Schemas para a API de Pergunta/Resposta (/ask)
# ==========================================

class Citation(BaseModel):
    """Citação do trecho utilizado para fundamentar a resposta da LLM."""
    document_id: str
    page_number: Optional[int] = None
    snippet: str


class QueryRequest(BaseModel):
    """Payload da requisição do usuário enviada para o endpoint /ask."""
    question: str = Field(..., min_length=3, description="Pergunta do usuário")
    top_k: Optional[int] = Field(default=None, description="Quantidade de chunks a recuperar")


class QueryResponse(BaseModel):
    """Resposta final da API ao usuário contendo resposta e fontes."""
    question: str
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Schemas de Health Check
# ==========================================

class HealthResponse(BaseModel):
    """Status de saúde da aplicação."""
    status: str = "ok"
    app_name: str
    environment: str