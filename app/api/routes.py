from pathlib import Path
import shutil
import tempfile

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.core.config import settings
from app.core.models import (
    QueryRequest,
    QueryResponse,
    DocumentUploadResponse,
    HealthResponse,
)
from app.api.deps import (
    get_ingestion_service,
    get_retrieval_service,
    get_generation_service,
)
from app.services.ingestion import IngestionService
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        environment=settings.ENV,
    )


@router.post("/documents", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    allowed_extensions = [".pdf", ".txt", ".md"]
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão não suportada. Envie um ficheiro: {', '.join(allowed_extensions)}",
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = Path(tmp_file.name)

        chunks_count = ingestion_service.ingest_file(tmp_path)
        tmp_path.unlink(missing_ok=True)

        return DocumentUploadResponse(
            filename=file.filename,
            chunks_created=chunks_count,
            message="Documento ingerido e indexado com sucesso.",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o documento: {str(exc)}",
        ) from exc


@router.post("/ask", response_model=QueryResponse, tags=["RAG"])
async def ask_question(
    request: QueryRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    generation_service: GenerationService = Depends(get_generation_service),
):
    try:
        chunks_recuperados = retrieval_service.retrieve_context(
            query=request.question,
            top_k=request.top_k,
        )
        response = generation_service.generate_answer(
            question=request.question,
            context_chunks=chunks_recuperados,
        )
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar a resposta: {str(exc)}",
        ) from exc
