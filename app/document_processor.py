"""
Document processing with support for multiple formats
Handles PDFs, text files, and includes error handling
"""

import PyPDF2
from pathlib import Path
from typing import List, Dict
from app.logger import logger
from app.config import Config


class DocumentProcessor:
    """Process documents for indexing"""

    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        """
        Extract text from PDF with error handling
        Handles corrupted PDFs gracefully
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    logger.error(f"PDF is encrypted: {file_path.name}")
                    raise ValueError("PDF is encrypted and cannot be processed")

                # Extract text from all pages
                for page_num in range(len(pdf_reader.pages)):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        text += page_text + "\n\n"
                    except Exception as e:
                        logger.warning(f"Error reading page {page_num + 1}: {e}")
                        continue

                if not text.strip():
                    raise ValueError("No text could be extracted from PDF")

                logger.info(f"Extracted {len(text)} characters from {file_path.name}")
                return text

        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"Corrupted PDF: {file_path.name} - {e}")
            raise ValueError(f"PDF file is corrupted: {str(e)}")

        except Exception as e:
            logger.error(f"Error processing PDF {file_path.name}: {e}")
            raise

    @staticmethod
    def extract_text_from_txt(file_path: Path) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            if not text.strip():
                raise ValueError("Text file is empty")

            logger.info(f"Read {len(text)} characters from {file_path.name}")
            return text

        except UnicodeDecodeError:
            # Try different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                return text
            except Exception as e:
                logger.error(f"Error reading text file {file_path.name}: {e}")
                raise

        except Exception as e:
            logger.error(f"Error processing text file {file_path.name}: {e}")
            raise

    @staticmethod
    def process_document(file_path: Path) -> str:
        """
        Process any supported document format
        Returns extracted text
        """

        file_extension = file_path.suffix.lower().replace('.', '')

        if file_extension not in Config.ALLOWED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {file_extension}")

        if file_extension == 'pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_extension == 'txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"No processor for file type: {file_extension}")

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks for better search results
        Overlap ensures context isn't lost at chunk boundaries
        """

        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])

            if chunk.strip():
                chunks.append({
                    'text': chunk,
                    'start_index': i,
                    'end_index': min(i + chunk_size, len(words))
                })

        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks

    @staticmethod
    def validate_file(file_path: Path) -> tuple[bool, str]:
        """
        Validate file before processing
        Checks size, type, existence
        """

        # Check if file exists
        if not file_path.exists():
            return False, "File does not exist"

        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > Config.MAX_FILE_SIZE_MB:
            return False, f"File too large: {file_size_mb:.2f}MB (max: {Config.MAX_FILE_SIZE_MB}MB)"

        # Check file type
        file_extension = file_path.suffix.lower().replace('.', '')
        if file_extension not in Config.ALLOWED_FILE_TYPES:
            return False, f"Unsupported file type: {file_extension}"

        return True, "Valid"