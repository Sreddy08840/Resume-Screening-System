
"""Text cleaning utility with email and phone number preservation."""
import re
from typing import List, Tuple


class TextCleaner:
    """
    A utility class for cleaning text content from resumes.
    Preserves emails and phone numbers during cleaning process.
    """

    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b')

    @staticmethod
    def _extract_preserve(text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Extracts and temporarily replaces emails and phone numbers with tokens.

        Args:
            text: Input text to process.

        Returns:
            Tuple containing processed text and list of (token, original_value) pairs.
        """
        preserved = []

        # Extract and replace emails
        def replace_email(match: re.Match) -> str:
            token = f"###EMAIL###{len(preserved)}###"
            preserved.append((token, match.group(0)))
            return token

        text = TextCleaner.EMAIL_PATTERN.sub(replace_email, text)

        # Extract and replace phone numbers
        def replace_phone(match: re.Match) -> str:
            token = f"###PHONE###{len(preserved)}###"
            preserved.append((token, match.group(0)))
            return token

        text = TextCleaner.PHONE_PATTERN.sub(replace_phone, text)

        return text, preserved

    @staticmethod
    def _restore_preserve(text: str, preserved: List[Tuple[str, str]]) -> str:
        """
        Restores preserved emails and phone numbers from tokens.

        Args:
            text: Text containing tokens.
            preserved: List of (token, original_value) pairs.

        Returns:
            Text with original values restored.
        """
        for token, original in preserved:
            text = text.replace(token, original)
        return text

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalizes whitespace by removing extra spaces, tabs, and excessive line breaks.

        Args:
            text: Text to normalize.

        Returns:
            Whitespace-normalized text.
        """
        if not text:
            return ""

        # Remove tabs
        text = re.sub(r'\t+', ' ', text)

        # Collapse multiple consecutive newlines
        text = re.sub(r'\n\s*\n+', '\n', text)

        # Remove duplicate whitespace within lines
        text = re.sub(r'[ \t]+', ' ', text)

        return text.strip()

    @staticmethod
    def clean(text: str) -> str:
        """
        Cleans text while preserving emails and phone numbers.

        Removes control characters, normalizes whitespace, and preserves
        important contact information.

        Args:
            text: Raw text to clean.

        Returns:
            Cleaned text.
        """
        if not text:
            return ""

        # Step 1: Extract and preserve emails and phone numbers
        text, preserved = TextCleaner._extract_preserve(text)

        # Step 2: Remove control characters
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)

        # Step 3: Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Step 4: Remove extra spaces
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+', '\n', text)

        # Step 5: Trim whitespace
        text = text.strip()

        # Step 6: Restore preserved content
        text = TextCleaner._restore_preserve(text, preserved)

        return text

    @staticmethod
    def minimal_clean(text: str) -> str:
        """
        Performs lightweight cleaning by normalizing only whitespace.

        Args:
            text: Text to clean.

        Returns:
            Whitespace-normalized text.
        """
        if not text:
            return ""
        return TextCleaner.normalize_whitespace(text)
