import sys
from pathlib import Path

# Adiciona a raiz do projeto para evitar o erro "No module named 'app.core'"
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import DocChatException
from app.core.logging import logger
from app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="API REST para consulta de documentos via RAG",
        version="1.0.0",
    )

    @app.exception_handler(DocChatException)
    async def docchat_exception_handler(request: Request, exc: DocChatException):
        logger.error(f"Erro de domínio capturado: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": exc.message},
        )

    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api.main:app", host="127.0.0.1", port=8000, reload=True)
