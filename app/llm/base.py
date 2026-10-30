from abc import ABC, abstractmethod
from typing import List, Optional


class LLMProvider(ABC):
    """Interface abstrata para provedores de LLM."""

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Gera uma resposta de texto a partir de um prompt e um system prompt opcional."""
        pass