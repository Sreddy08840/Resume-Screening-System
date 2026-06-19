
"""Weighted scoring logic combining skill and experience scores."""
from dataclasses import dataclass
from typing import Dict, Any
from models.candidate import Candidate
from models.job import Job
from matcher.skill_matcher import SkillMatcher, SkillMatchResult
from matcher.experience_matcher import ExperienceMatcher, ExperienceMatchResult
from config import Config


@dataclass
class ScoreResult:
    """
    Result of final scoring process for a candidate.

    Attributes:
        skill_result: Detailed skill matching result.
        experience_result: Detailed experience matching result.
        skill_score: Skill component of final score (0-100).
        experience_score: Experience component of final score (0-100).
        final_score: Weighted final score (0-100).
    """

    skill_result: SkillMatchResult
    experience_result: ExperienceMatchResult
    skill_score: float
    experience_score: float
    final_score: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts result to a dictionary for serialization.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "skill_result": self.skill_result.to_dict(),
            "experience_result": self.experience_result.to_dict(),
            "skill_score": self.skill_score,
            "experience_score": self.experience_score,
            "final_score": self.final_score,
        }


class Scorer:
    """Calculates final candidate score using weighted formula."""

    @staticmethod
    def calculate_score(candidate: Candidate, job: Job) -> ScoreResult:
        """
        Calculates final score using configured weights.

        Formula:
            Final Score = (skill_score * SKILL_WEIGHT) + (experience_score * EXPERIENCE_WEIGHT)

        Args:
            candidate: Candidate to score.
            job: Job requirements.

        Returns:
            ScoreResult with detailed score components.
        """
        # Calculate individual scores
        skill_result = SkillMatcher.match(candidate.skills, job.required_skills)
        experience_result = ExperienceMatcher.match(
            candidate.raw_text or "", job.minimum_experience
        )

        # Calculate final score with weights (rounded)
        skill_score = round(skill_result.skill_score)
        experience_score = round(experience_result.experience_score)
        final_score = round(
            skill_score * Config.SKILL_WEIGHT + experience_score * Config.EXPERIENCE_WEIGHT
        )

        return ScoreResult(
            skill_result=skill_result,
            experience_result=experience_result,
            skill_score=skill_score,
            experience_score=experience_score,
            final_score=final_score,
        )
