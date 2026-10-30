from typing import List
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.logging import logger


class EmbeddingService:
    """Wrapper para geração de embeddings vetoriais."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        logger.info(f"A carregar modelo de embeddings: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)

    def embed_text(self, text: str) -> List[float]:
        """Gera o vetor de embedding para um único texto."""
        return self.model.encode(text).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Gera vetores de embeddings para uma lista de textos."""
        return self.model.encode(texts).tolist()