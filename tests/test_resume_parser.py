
import os
import pytest
from parser.resume_parser import ResumeParser
from parser.txt_parser import TXTParser
from parser.exceptions import EmptyFileError, UnsupportedFileTypeError


class TestResumeParser:
    """Test suite for ResumeParser class."""

    def test_parse_single_txt(self, test_data_dir, sample_resume_content):
        """Test parsing a single valid TXT resume."""
        resume_path = os.path.join(test_data_dir, "resumes", "test_resume.txt")
        with open(resume_path, "w", encoding="utf-8") as f:
            f.write(sample_resume_content)
        
        result = ResumeParser.parse_single(resume_path)
        
        assert result["success"] is True
        assert "John Doe" in result["raw_text"]

    def test_parse_multiple(self, test_data_dir, sample_resume_content):
        """Test parsing multiple resumes."""
        resumes_dir = os.path.join(test_data_dir, "resumes")
        
        # Clear any existing files
        for filename in os.listdir(resumes_dir):
            os.remove(os.path.join(resumes_dir, filename))
        
        # Create test files
        for i in range(3):
            path = os.path.join(resumes_dir, f"resume{i}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(sample_resume_content)
        
        results = ResumeParser.parse_multiple(resumes_dir)
        
        assert len(results) == 3
        assert all(r["success"] is True for r in results)

    def test_parse_empty_file(self, test_data_dir):
        """Test parsing an empty file."""
        empty_path = os.path.join(test_data_dir, "resumes", "empty.txt")
        with open(empty_path, "w") as f:
            pass
        
        result = ResumeParser.parse_single(empty_path)
        
        assert result["success"] is False
        assert "Empty" in result["error"]

    def test_parse_unsupported_file(self, test_data_dir):
        """Test parsing an unsupported file type."""
        unsupported_path = os.path.join(test_data_dir, "resumes", "test.zip")
        with open(unsupported_path, "w", encoding="utf-8") as f:
            f.write("test")
        
        result = ResumeParser.parse_single(unsupported_path)
        
        assert result["success"] is False
        assert "Unsupported" in result["error"]

    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file."""
        result = ResumeParser.parse_single("/path/does/not/exist.txt")
        
        assert result["success"] is False
        assert "not found" in result["error"]


class TestTXTParser:
    """Test suite for TXTParser class."""

    def test_parse_valid_txt(self, sample_resume_content, test_data_dir):
        """Test parsing valid TXT file."""
        path = os.path.join(test_data_dir, "resumes", "test.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(sample_resume_content)
        
        text = TXTParser.parse(path)
        
        assert "John Doe" in text

    def test_empty_txt_raises_error(self, test_data_dir):
        """Test that empty TXT file raises EmptyFileError."""
        path = os.path.join(test_data_dir, "resumes", "empty2.txt")
        with open(path, "w") as f:
            pass
        
        with pytest.raises(EmptyFileError):
            TXTParser.parse(path)

