import pytest
from matcher.experience_matcher import ExperienceMatcher


class TestExperienceMatcher:
    """Test suite for ExperienceMatcher class."""

    def test_extract_years_valid(self):
        """Test extracting years of experience from text."""
        test_cases = [
            ("Experience: 8 years", 8),
            ("5+ years of experience", 5),
            ("10 years working in this field", 10),
            ("No experience", 0),
            ("", 0),
        ]

        for text, expected in test_cases:
            assert ExperienceMatcher.extract_years(text) == expected

    def test_calculate_score_meets_or_exceeds(self):
        """Test when experience meets or exceeds minimum."""
        assert ExperienceMatcher.calculate_score(8, 2) == 100.0
        assert ExperienceMatcher.calculate_score(2, 2) == 100.0

    def test_calculate_score_half(self):
        """Test when experience is half minimum."""
        assert ExperienceMatcher.calculate_score(1, 2) == 50.0

    def test_calculate_score_zero(self):
        """Test when experience is zero."""
        assert ExperienceMatcher.calculate_score(0, 2) == 0.0

    def test_match(self):
        """Test the full match method."""
        text = "8 years of experience"
        minimum = 2

        result = ExperienceMatcher.match(text, minimum)

        assert result.candidate_years == 8
        assert result.required_years == 2
        assert result.experience_score == 100.0

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        text = "8 years of experience"
        minimum = 2

        result = ExperienceMatcher.match(text, minimum)
        result_dict = result.to_dict()

        assert "candidate_years" in result_dict
        assert "required_years" in result_dict
        assert "experience_score" in result_dict
