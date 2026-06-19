
import os
from parser.exceptions import InvalidPDFError, EmptyFileError
from config import logger


try:
    from PyPDF2 import PdfReader
    HAS_PYPDF = True
except ImportError:
    logger.warning("PyPDF2 not installed, PDF parsing limited")
    HAS_PYPDF = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    logger.warning("pdfplumber not installed, PDF parsing limited")
    HAS_PDFPLUMBER = False


class PDFParser:
    @staticmethod
    def parse(file_path: str) -> str:
        """
        Parse text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
            
        Raises:
            InvalidPDFError: If PDF is invalid or corrupted
            EmptyFileError: If PDF contains no text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        logger.debug(f"Parsing PDF file: {file_path}")
        
        # Try pdfplumber first for better text extraction
        if HAS_PDFPLUMBER:
            try:
                text = PDFParser._parse_with_pdfplumber(file_path)
                if text and text.strip():
                    logger.debug("Successfully parsed PDF with pdfplumber")
                    return text
            except Exception as e:
                logger.debug(f"pdfplumber failed: {e}, trying PyPDF2")
        
        # Try PyPDF2 as fallback
        if HAS_PYPDF:
            try:
                text = PDFParser._parse_with_pypdf2(file_path)
                if text and text.strip():
                    logger.debug("Successfully parsed PDF with PyPDF2")
                    return text
            except Exception as e:
                logger.error(f"PyPDF2 failed: {e}")
        
        # Both failed - invalid PDF
        raise InvalidPDFError(f"Unable to parse PDF file: {file_path}")
    
    @staticmethod
    def _parse_with_pypdf2(file_path: str) -> str:
        """Extract text using PyPDF2"""
        text_parts = []
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
        
        text = "\n".join(text_parts)
        if not text.strip():
            raise EmptyFileError("PDF file contains no text")
        return text
    
    @staticmethod
    def _parse_with_pdfplumber(file_path: str) -> str:
        """Extract text using pdfplumber (better extraction quality)"""
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        
        text = "\n".join(text_parts)
        if not text.strip():
            raise EmptyFileError("PDF file contains no text")
        return text

