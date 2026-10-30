from typing import Optional
import anthropic

from app.core.config import settings
from app.core.exceptions import LLMProviderError
from app.core.logging import logger
from app.llm.base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Implementação do provedor de LLM utilizando a API da Anthropic (Claude)."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.LLM_MODEL

        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY não foi configurada.")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        temp = temperature if temperature is not None else settings.LLM_TEMPERATURE
        max_tok = max_tokens if max_tokens is not None else settings.LLM_MAX_TOKENS

        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tok,
                "temperature": temp,
                "messages": [{"role": "user", "content": prompt}],
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            logger.info(f"Enviando requisição para a Anthropic (Modelo: {self.model})")
            response = self.client.messages.create(**kwargs)

            # Extrai o texto do primeiro bloco de conteúdo
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return ""

        except Exception as e:
            logger.error(f"Erro ao chamar a API da Anthropic: {str(e)}")
            raise LLMProviderError(f"Falha na geração de resposta via Anthropic: {str(e)}") from e