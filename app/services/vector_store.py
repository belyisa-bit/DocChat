from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.core.exceptions import VectorStoreError
from app.core.logging import logger


class VectorStoreService:
    """Gerenciador do banco de dados vetorial ChromaDB."""

    def __init__(self):
        try:
            settings.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=str(settings.CHROMA_PERSIST_DIRECTORY)
            )
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"ChromaDB inicializado na coleção '{settings.CHROMA_COLLECTION_NAME}'.")
        except Exception as e:
            logger.error(f"Erro ao inicializar ChromaDB: {str(e)}")
            raise VectorStoreError(f"Falha ao conectar com ChromaDB: {str(e)}") from e

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """Adiciona chunks e seus respetivos embeddings à coleção."""
        if not chunks:
            return

        ids = [c["id"] for c in chunks]
        documents = [c["content"] for c in chunks]
        metadatas = [
            {"document_id": c["document_id"], "page_number": c["page_number"]}
            for c in chunks
        ]

        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            logger.info(f"{len(chunks)} chunks inseridos no ChromaDB.")
        except Exception as e:
            logger.error(f"Erro ao inserir chunks no ChromaDB: {str(e)}")
            raise VectorStoreError(f"Falha na inserção no banco vetorial: {str(e)}") from e

    def search_similar(self, query_embedding: List[float], top_k: int = None) -> List[Dict[str, Any]]:
        """Busca os chunks mais similares ao vetor da query."""
        k = top_k or settings.RETRIEVAL_TOP_K
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )

            retrieved = []
            if results and results["ids"] and len(results["ids"][0]) > 0:
                for idx in range(len(results["ids"][0])):
                    # Converte distância cosseno em score de similaridade (1 - distância)
                    distance = results["distances"][0][idx] if results.get("distances") else 0.0
                    similarity_score = 1.0 - distance

                    retrieved.append({
                        "id": results["ids"][0][idx],
                        "content": results["documents"][0][idx],
                        "document_id": results["metadatas"][0][idx].get("document_id"),
                        "page_number": results["metadatas"][0][idx].get("page_number"),
                        "score": similarity_score
                    })

            return retrieved
        except Exception as e:
            logger.error(f"Erro ao realizar busca vetorial: {str(e)}")
            raise VectorStoreError(f"Falha na busca vetorial: {str(e)}") from e