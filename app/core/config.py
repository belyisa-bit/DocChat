import os


class Settings:
    APP_NAME = os.getenv("APP_NAME", "DocChat")
    ENV = os.getenv("APP_ENV", "dev")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
    LLM_MODEL = os.getenv("LLM_MODEL", "claude-3-haiku-20240307")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))


settings = Settings()
from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Aplicação
    APP_NAME: str = "DocChat RAG API"
    ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Provedores de LLM
    LLM_PROVIDER: Literal["anthropic"] = "anthropic"
    ANTHROPIC_API_KEY: str = Field(default="", description="Chave da API da Anthropic")
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 1000

    # Configurações de Embedding
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Configurações do Vector Store (ChromaDB)
    CHROMA_PERSIST_DIRECTORY: Path = Path("./chroma_db")
    CHROMA_COLLECTION_NAME: str = "docchat_collection"

    # Parâmetros de Chunking
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # Parâmetros de Retrieval
    RETRIEVAL_TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.3


# Instância global para importação direta no projeto
settings = Settings()
