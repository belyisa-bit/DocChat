class IngestionService:
    """Service responsible for ingesting documents into the knowledge base."""

    def ingest_file(self, file_path):
        return 1
from pathlib import Path
from app.services.loaders import load_document
from app.services.chunking import chunk_document_pages
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreService


class IngestionService:
    """Orquestra o fluxo de ingestão: Carregar -> Chunking -> Embedding -> Persistência."""

    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStoreService):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest_file(self, file_path: Path) -> int:
        pages = load_document(file_path)
        chunks = chunk_document_pages(pages)
        if not chunks:
            return 0

        texts = [c["content"] for c in chunks]
        embeddings = self.embedding_service.embed_documents(texts)
        self.vector_store.add_chunks(chunks, embeddings)

        return len(chunks)
