"""
Document Q&A Enterprise System
A production-ready enterprise document question-answering system
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from app.config import Config
from app.logger import logger
from app.search_service import AzureSearchService
from app.ai_service import AIService
from app.document_processor import DocumentProcessor
from app.safety_filter import SafetyFilter

__all__ = [
    'Config',
    'logger',
    'AzureSearchService',
    'AIService',
    'DocumentProcessor',
    'SafetyFilter'
]