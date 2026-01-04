"""
Centralized logging system with color output and file storage
Tracks all system operations for debugging and auditing
"""

import logging
import colorlog
from datetime import datetime
from pathlib import Path
from app.config import Config


class SystemLogger:
    """Enhanced logging system for enterprise use"""

    def __init__(self, name="DocumentQA"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        console_format = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler for persistent logs
        log_file = Config.LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """Log info message"""
        self.logger.info(message)

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message):
        """Log error message"""
        self.logger.error(message)

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

    def log_question(self, question, answer, sources=None):
        """Log a Q&A interaction for audit trail"""
        log_entry = f"Q: {question[:100]}... | A: {answer[:100]}..."
        if sources:
            log_entry += f" | Sources: {sources}"
        self.logger.info(f"QA_LOG - {log_entry}")

    def log_document_upload(self, filename, status, error=None):
        """Log document upload events"""
        if status == "success":
            self.logger.info(f"DOC_UPLOAD - Success: {filename}")
        else:
            self.logger.error(f"DOC_UPLOAD - Failed: {filename} - Error: {error}")

    def log_error(self, operation, error):
        """Log errors with context"""
        self.logger.error(f"ERROR - {operation}: {str(error)}")


# Global logger instance
logger = SystemLogger()