from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

from app.core.exceptions import DocumentProcessingError
from app.core.logging import logger


def load_document(file_path: Path) -> List[Dict[str, Any]]:
    """Lê um ficheiro (PDF, TXT ou MD) e retorna uma lista de páginas/seções com metadados."""
    if not file_path.exists():
        raise DocumentProcessingError(f"Ficheiro não encontrado: {file_path}")

    ext = file_path.suffix.lower()
    pages = []

    try:
        if ext == ".pdf":
            reader = PdfReader(file_path)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({
                        "content": text,
                        "page_number": idx + 1,
                        "source": file_path.name
                    })

        elif ext in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    pages.append({
                        "content": text,
                        "page_number": 1,
                        "source": file_path.name
                    })

        else:
            raise DocumentProcessingError(f"Formato de ficheiro não suportado: {ext}")

        logger.info(f"Ficheiro {file_path.name} carregado com {len(pages)} páginas/blocos.")
        return pages

    except Exception as e:
        logger.error(f"Erro ao carregar documento {file_path}: {str(e)}")
        raise DocumentProcessingError(f"Falha na leitura do ficheiro: {str(e)}") from e