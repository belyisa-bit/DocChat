from app.core.config import settings
from app.core.exceptions import LLMProviderError
from app.llm.anthropic_provider import AnthropicProvider
from app.llm.base import LLMProvider


def get_llm_provider() -> LLMProvider:
    """Factory function que retorna a instância do provedor de LLM configurado."""
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == "anthropic":
        return AnthropicProvider()
    
    raise LLMProviderError(f"Provedor de LLM não suportado: '{provider_name}'")