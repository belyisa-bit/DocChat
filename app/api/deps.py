from app.services.generation import GenerationService
from app.services.ingestion import IngestionService
from app.services.retrieval import RetrievalService


def get_ingestion_service() -> IngestionService:
    return IngestionService()


def get_retrieval_service() -> RetrievalService:
    return RetrievalService()


def get_generation_service() -> GenerationService:
    return GenerationService()
