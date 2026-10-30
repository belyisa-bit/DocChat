from typing import List, Dict, Any

from app.core.models import Citation, QueryResponse
from app.llm.base import LLMProvider


class GenerationService:
    """Orquestra a montagem de prompt, chamada à LLM e geração de citações."""

    SYSTEM_PROMPT = (
        "Você é um assistente preciso de análise de documentos. "
        "Responda à pergunta do usuário utilizando APENAS as informações fornecidas no contexto abaixo. "
        "Se o contexto não contiver informação suficiente para responder à pergunta, responda exatamente: "
        "'Não encontrei informações suficientes nos documentos fornecidos para responder a essa pergunta.' "
        "Não invente e nem use conhecimento externo."
    )

    def __init__(self, llm_provider: LLMProvider = None):
        self.llm = llm_provider or self._build_default_llm()

    def _build_default_llm(self):
        from app.llm.factory import get_llm_provider
        return get_llm_provider()

    def generate_answer(self, question: str, context_chunks: List[Dict[str, Any]]) -> QueryResponse:
        if not context_chunks:
            return QueryResponse(
                question=question,
                answer="Não encontrei informações suficientes nos documentos fornecidos para responder a essa pergunta.",
                citations=[]
            )

        context_text = "\n\n---\n\n".join(
            [f"[Documento: {c['document_id']} | Página: {c['page_number']}]\n{c['content']}" for c in context_chunks]
        )

        user_prompt = f"Contexto:\n{context_text}\n\nPergunta: {question}"

        raw_answer = self.llm.generate_response(
            prompt=user_prompt,
            system_prompt=self.SYSTEM_PROMPT
        )

        citations = [
            Citation(
                document_id=c["document_id"],
                page_number=c.get("page_number"),
                snippet=c["content"][:150] + "..." if len(c["content"]) > 150 else c["content"]
            )
            for c in context_chunks
        ]

        return QueryResponse(
            question=question,
            answer=raw_answer,
            citations=citations
        )
