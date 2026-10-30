from typing import List, Dict, Any
from app.core.config import settings
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreService


class RetrievalService:
    """Serviço responsável por recuperar contexto relevante aplicando limiar de similaridade."""

    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStoreService):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve_context(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        query_vector = self.embedding_service.embed_text(query)
        results = self.vector_store.search_similar(query_vector, top_k=top_k)

        # Filtra chunks pelo limiar mínimo de similaridade configurado
        filtered_results = [
            doc for doc in results
            if doc.get("score", 0.0) >= settings.SIMILARITY_THRESHOLD
        ]

        return filtered_filtered_results if 'filtered_filtered_results' in locals() else filtered_results