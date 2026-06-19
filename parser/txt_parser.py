
import os
from parser.exceptions import EmptyFileError
from config import logger


class TXTParser:
    @staticmethod
    def parse(file_path: str) -> str:
        """
        Parse text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Extracted text
            
        Raises:
            EmptyFileError: If TXT file is empty
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TXT file not found: {file_path}")
        
        logger.debug(f"Parsing TXT file: {file_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                
                if not text.strip():
                    logger.warning("TXT file contains no text")
                    raise EmptyFileError("TXT file is empty")
                
                logger.debug(f"Successfully parsed TXT with {encoding} encoding")
                return text
            
            except UnicodeDecodeError:
                logger.debug(f"Failed to decode with {encoding}, trying next encoding")
                continue
        
        # All encodings failed
        raise Exception("Unable to decode TXT file with any supported encoding")

