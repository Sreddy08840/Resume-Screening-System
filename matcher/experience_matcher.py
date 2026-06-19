
"""Experience matching logic for candidate and job requirement comparison."""
from typing import Dict, Any
from utils.regex_patterns import YEARS_EXPERIENCE_PATTERN


class ExperienceMatchResult:
    """
    Result data from experience matching process.

    Attributes:
        candidate_years: Years of experience extracted from candidate.
        required_years: Minimum required years for the job.
        experience_score: Calculated experience score (0-100).
    """

    def __init__(self) -> None:
        self.candidate_years: int = 0
        self.required_years: int = 0
        self.experience_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts result to a dictionary for serialization.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "candidate_years": self.candidate_years,
            "required_years": self.required_years,
            "experience_score": self.experience_score,
        }


class ExperienceMatcher:
    """
    Matches candidate experience with job requirements.
    Extracts years of experience from text and calculates score.
    """

    @staticmethod
    def extract_years(candidate_text: str) -> int:
        """
        Extracts years of experience from candidate text using regex.

        Args:
            candidate_text: Raw text from candidate's resume.

        Returns:
            Maximum number of years of experience found.
        """
        matches = YEARS_EXPERIENCE_PATTERN.findall(candidate_text)
        if matches:
            return max(int(m) for m in matches)
        return 0

    @staticmethod
    def calculate_score(candidate_years: int, required_years: int) -> float:
        """
        Calculates experience score based on candidate vs required years.

        Scoring rules:
            - If no experience required: 100
            - If candidate meets or exceeds required: 100
            - If candidate is below: percentage score

        Args:
            candidate_years: Years of experience the candidate has.
            required_years: Minimum required years.

        Returns:
            Experience score (0-100).
        """
        if required_years <= 0:
            return 100.0

        if candidate_years >= required_years:
            return 100.0

        return (candidate_years / required_years) * 100

    @staticmethod
    def match(candidate_text: str, required_years: int) -> ExperienceMatchResult:
        """
        Matches candidate experience with required experience.

        Args:
            candidate_text: Raw text from candidate's resume.
            required_years: Minimum required years of experience.

        Returns:
            ExperienceMatchResult with candidate years and score.
        """
        result = ExperienceMatchResult()
        result.required_years = required_years
        result.candidate_years = ExperienceMatcher.extract_years(candidate_text)
        result.experience_score = ExperienceMatcher.calculate_score(
            result.candidate_years, required_years
        )

        return result
