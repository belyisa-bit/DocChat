class DocChatException(Exception):
    """Exceção base para o projeto DocChat."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DocumentProcessingError(DocChatException):
    """Lançada quando ocorre um erro na leitura ou chunking do documento."""
    pass


class VectorStoreError(DocChatException):
    """Lançada em falhas de operação com o ChromaDB."""
    pass


class LLMProviderError(DocChatException):
    """Lançada quando a chamada à API do LLM falha."""
    pass


class RetrievalError(DocChatException):
    """Lançada em falhas no processo de busca/recuperação de contexto."""
    pass