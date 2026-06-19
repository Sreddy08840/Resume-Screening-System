
"""Skill matching logic for comparing candidate skills with job requirements."""
from typing import List, Dict, Any, Set
import re


class SkillMatchResult:
    """
    Result data from skill matching process.

    Attributes:
        matched_skills: List of skills the candidate has that match requirements.
        missing_skills: List of skills the candidate is missing.
        skill_percentage: Percentage of required skills matched (0-100).
        skill_score: Calculated skill score (0-100).
    """

    def __init__(self) -> None:
        self.matched_skills: List[str] = []
        self.missing_skills: List[str] = []
        self.skill_percentage: float = 0.0
        self.skill_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts result to a dictionary for serialization.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "skill_percentage": self.skill_percentage,
            "skill_score": self.skill_score,
        }


class SkillMatcher:
    """
    Matches candidate skills with required job skills.
    Supports exact and partial matching.
    """

    @staticmethod
    def _normalize_skills(skills: List[str]) -> Set[str]:
        """
        Normalizes skills by lowercasing, trimming, and deduplicating.

        Args:
            skills: List of raw skills.

        Returns:
            Normalized, deduplicated set of skills.
        """
        normalized = set()
        for skill in skills:
            if skill:
                normalized.add(skill.strip().lower())
        return normalized

    @staticmethod
    def _is_partial_match(required_skill: str, candidate_skill: str) -> bool:
        """
        Checks for partial match between two skills (substring matching).

        Args:
            required_skill: Required skill.
            candidate_skill: Candidate skill.

        Returns:
            True if partial match exists, False otherwise.
        """
        req = required_skill.lower()
        cand = candidate_skill.lower()
        return req in cand or cand in req

    @staticmethod
    def match(
        candidate_skills: List[str], required_skills: List[str], partial_match: bool = True
    ) -> SkillMatchResult:
        """
        Matches candidate skills with required job skills.

        Args:
            candidate_skills: Skills extracted from candidate resume.
            required_skills: Skills required for the job.
            partial_match: Whether to allow partial (substring) matches.

        Returns:
            SkillMatchResult with matched/missing skills and score.
        """
        result = SkillMatchResult()

        if not required_skills:
            result.skill_percentage = 100.0
            result.skill_score = 100.0
            return result

        # Normalize skills
        candidate_skills_normalized = SkillMatcher._normalize_skills(candidate_skills)
        required_skills_normalized = SkillMatcher._normalize_skills(required_skills)

        matched_count = 0
        matched_skills_set = set()

        for req_skill in required_skills_normalized:
            found = False

            # Check exact match first
            if req_skill in candidate_skills_normalized:
                found = True
                matched_skills_set.add(req_skill)
            elif partial_match:
                # Check partial matches
                for cand_skill in candidate_skills_normalized:
                    if SkillMatcher._is_partial_match(req_skill, cand_skill):
                        found = True
                        matched_skills_set.add(req_skill)
                        break

            # Find original case for display
            original_req = next(
                (s for s in required_skills if s.lower() == req_skill),
                req_skill.title(),
            )

            if found:
                matched_count += 1
                result.matched_skills.append(original_req)
            else:
                result.missing_skills.append(original_req)

        # Calculate percentage and score
        total_required = len(required_skills_normalized)
        result.skill_percentage = (matched_count / total_required) * 100
        result.skill_score = round(result.skill_percentage, 2)

        return result
