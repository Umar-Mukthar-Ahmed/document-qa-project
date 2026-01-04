"""
Configuration management for the enterprise Q&A system
Loads and validates all environment variables
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    LOGS_DIR = DATA_DIR / "logs"

    # Ensure directories exist
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Azure Search Configuration
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "enterprise-documents")

    # Application Settings
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "pdf,txt").split(",")

    # Safety Settings
    ENABLE_CONTENT_FILTER = os.getenv("ENABLE_CONTENT_FILTER", "true").lower() == "true"
    MAX_QUESTION_LENGTH = int(os.getenv("MAX_QUESTION_LENGTH", "500"))

    # AI Settings
    AI_TEMPERATURE = 0.2
    AI_MAX_TOKENS = 500
    SEARCH_TOP_K = 3

    @classmethod
    def validate(cls):
        """Validate that all required configurations are set"""
        errors = []

        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")

        if not cls.AZURE_SEARCH_ENDPOINT:
            errors.append("AZURE_SEARCH_ENDPOINT is not set")

        if not cls.AZURE_SEARCH_API_KEY:
            errors.append("AZURE_SEARCH_API_KEY is not set")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True


# Validate configuration on import
Config.validate()