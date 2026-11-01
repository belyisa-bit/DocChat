from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logging import logger


def chunk_document_pages(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Divide o conteúdo de páginas em chunks menores mantendo metadados."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
    )

    chunks = []
    chunk_counter = 0

    for page in pages:
        split_texts = splitter.split_text(page["content"])
        for idx, text in enumerate(split_texts):
            chunk_counter += 1
            chunks.append({
                "id": f"{page['source']}_p{page['page_number']}_c{idx}",
                "content": text,
                "document_id": page["source"],
                "page_number": page["page_number"]
            })

    logger.info(f"Gerados {len(chunks)} chunks a partir de {len(pages)} páginas.")
    return chunks