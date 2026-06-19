
class ResumeParserError(Exception):
    """Base exception for resume parser errors"""
    pass


class UnsupportedFileTypeError(ResumeParserError):
    """Raised when the file type is not supported"""
    pass


class CorruptedFileError(ResumeParserError):
    """Raised when a file is corrupted or unreadable"""
    pass


class EmptyFileError(ResumeParserError):
    """Raised when a file is empty or contains no text"""
    pass


class InvalidPDFError(CorruptedFileError):
    """Raised when PDF file is invalid or corrupted"""
    pass


class InvalidDOCXError(CorruptedFileError):
    """Raised when DOCX file is invalid or corrupted"""
    pass

