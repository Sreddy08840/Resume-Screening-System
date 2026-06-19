
import os
from parser.pdf_parser import PDFParser
from parser.docx_parser import DOCXParser
from parser.txt_parser import TXTParser
from parser.text_cleaner import TextCleaner
from parser.exceptions import (
    ResumeParserError,
    UnsupportedFileTypeError,
    CorruptedFileError,
    EmptyFileError
)
from config import logger


class ResumeParser:
    @staticmethod
    def _get_parser(file_path: str):
        """Get appropriate parser based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return PDFParser
        elif ext == '.docx':
            return DOCXParser
        elif ext == '.txt':
            return TXTParser
        else:
            raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")
    
    @staticmethod
    def parse_single(file_path: str) -> dict:
        """
        Parse a single resume file
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dict with 'success' (bool), 'text' (str if success), 'error' (str if failed)
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': 'File not found'
            }
        
        if not os.path.isfile(file_path):
            logger.error(f"Not a file: {file_path}")
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': 'Not a file'
            }
        
        logger.info(f"Parsing resume: {os.path.basename(file_path)}")
        
        try:
            # Check file type first
            parser = ResumeParser._get_parser(file_path)
            
            # Validate file size
            if os.path.getsize(file_path) == 0:
                logger.warning(f"Empty file: {file_path}")
                return {
                    'success': False,
                    'file': os.path.basename(file_path),
                    'error': 'Empty file'
                }
            
            # Extract text
            raw_text = parser.parse(file_path)
            
            # Clean text
            cleaned_text = TextCleaner.clean(raw_text)
            
            logger.info(f"Successfully parsed: {os.path.basename(file_path)}")
            return {
                'success': True,
                'file': os.path.basename(file_path),
                'raw_text': raw_text,
                'cleaned_text': cleaned_text
            }
        
        except UnsupportedFileTypeError as e:
            logger.error(f"Unsupported file type for {os.path.basename(file_path)}: {e}")
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': 'Unsupported file type'
            }
        except EmptyFileError as e:
            logger.error(f"Empty file {os.path.basename(file_path)}: {e}")
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': 'File contains no text'
            }
        except CorruptedFileError as e:
            logger.error(f"Corrupted file {os.path.basename(file_path)}: {e}")
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': 'File is corrupted or unreadable'
            }
        except Exception as e:
            logger.error(f"Unexpected error parsing {os.path.basename(file_path)}: {e}", exc_info=True)
            return {
                'success': False,
                'file': os.path.basename(file_path),
                'error': f'Unexpected error: {str(e)}'
            }
    
    @staticmethod
    def parse_multiple(directory: str) -> list:
        """
        Parse all resume files in a directory
        
        Args:
            directory: Directory containing resume files
            
        Returns:
            List of parse results
        """
        if not os.path.exists(directory):
            logger.error(f"Directory not found: {directory}")
            return []
        
        if not os.path.isdir(directory):
            logger.error(f"Not a directory: {directory}")
            return []
        
        logger.info(f"Parsing all resumes in directory: {directory}")
        
        results = []
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                result = ResumeParser.parse_single(file_path)
                results.append(result)
        
        logger.info(f"Parsed {len(results)} files, {sum(1 for r in results if r['success'])} successful")
        return results

