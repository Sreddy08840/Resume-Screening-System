
import pytest
from parser.text_cleaner import TextCleaner


class TestTextCleaner:
    """Test suite for TextCleaner class."""

    def test_remove_extra_spaces(self):
        """Test removing extra spaces."""
        text = "  Hello   world!  "
        cleaned = TextCleaner.clean(text)
        assert "  " not in cleaned
        assert cleaned == "Hello world!"

    def test_remove_tabs(self):
        """Test removing tabs."""
        text = "\tHello\tworld!\t"
        cleaned = TextCleaner.clean(text)
        assert "\t" not in cleaned

    def test_remove_unnecessary_line_breaks(self):
        """Test removing unnecessary line breaks."""
        text = "Hello\n\n\nworld!"
        cleaned = TextCleaner.clean(text)
        assert "\n\n\n" not in cleaned

    def test_preserve_emails(self):
        """Test that emails are preserved during cleaning."""
        email = "test.user@example-domain.co.uk"
        text = f"Contact {email} for info"
        cleaned = TextCleaner.clean(text)
        assert email in cleaned

    def test_preserve_phone_numbers(self):
        """Test that phone numbers are preserved during cleaning."""
        phone = "(555) 123-4567"
        text = f"Call {phone} today"
        cleaned = TextCleaner.clean(text)
        assert phone in cleaned

    def test_minimal_clean(self):
        """Test minimal cleaning method."""
        text = "  \tHello world\n\n\t"
        cleaned = TextCleaner.minimal_clean(text)
        assert cleaned == "Hello world"

    def test_empty_text(self):
        """Test cleaning empty text."""
        cleaned = TextCleaner.clean("")
        assert cleaned == ""
        cleaned = TextCleaner.minimal_clean("")
        assert cleaned == ""

    def test_control_characters(self):
        """Test removing control characters."""
        text = "Hello\x00world\x01!"
        cleaned = TextCleaner.clean(text)
        assert "\x00" not in cleaned
        assert "\x01" not in cleaned

