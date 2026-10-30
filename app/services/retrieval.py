class RetrievalService:
    """Minimal retrieval service used by the API when a vector store is not available."""

    def retrieve_context(self, query: str, top_k: int = 3):
        return []
