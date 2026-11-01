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
