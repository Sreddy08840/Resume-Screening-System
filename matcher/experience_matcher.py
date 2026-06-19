
from typing import Optional
from utils.regex_patterns import YEARS_EXPERIENCE_PATTERN


class ExperienceMatchResult:
    def __init__(self):
        self.candidate_years: int = 0
        self.required_years: int = 0
        self.experience_score: float = 0.0
    
    def to_dict(self):
        return {
            'candidate_years': self.candidate_years,
            'required_years': self.required_years,
            'experience_score': self.experience_score
        }


class ExperienceMatcher:
    @staticmethod
    def extract_years(candidate_text: str) -> int:
        """Extract years of experience from candidate text"""
        matches = YEARS_EXPERIENCE_PATTERN.findall(candidate_text)
        if matches:
            return max(int(m) for m in matches)
        return 0
    
    @staticmethod
    def calculate_score(candidate_years: int, required_years: int) -> float:
        """
        Calculate experience score based on candidate vs required years
        
        Args:
            candidate_years: Number of years candidate has
            required_years: Minimum required years
            
        Returns:
            Score from 0 to 100
        """
        if required_years <= 0:
            return 100.0
        
        if candidate_years >= required_years:
            return 100.0
        
        return (candidate_years / required_years) * 100
    
    @staticmethod
    def match(candidate_text: str, required_years: int) -> ExperienceMatchResult:
        """
        Match candidate experience with required experience
        
        Args:
            candidate_text: Raw text from candidate resume
            required_years: Minimum required years of experience
            
        Returns:
            ExperienceMatchResult with candidate years, required years, and score
        """
        result = ExperienceMatchResult()
        result.required_years = required_years
        result.candidate_years = ExperienceMatcher.extract_years(candidate_text)
        result.experience_score = ExperienceMatcher.calculate_score(
            result.candidate_years, required_years
        )
        
        return result
