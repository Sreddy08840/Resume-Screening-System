
from dataclasses import dataclass
from typing import Dict, Any
from models.candidate import Candidate
from models.job import Job
from matcher.skill_matcher import SkillMatcher, SkillMatchResult
from matcher.experience_matcher import ExperienceMatcher, ExperienceMatchResult
from config import Config


@dataclass
class ScoreResult:
    skill_result: SkillMatchResult
    experience_result: ExperienceMatchResult
    skill_score: float
    experience_score: float
    final_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_result": self.skill_result.to_dict(),
            "experience_result": self.experience_result.to_dict(),
            "skill_score": self.skill_score,
            "experience_score": self.experience_score,
            "final_score": self.final_score
        }


class Scorer:
    @staticmethod
    def calculate_score(candidate: Candidate, job: Job) -> ScoreResult:
        """
        Calculate final score using the formula:
        Final Score = 0.7 × Skill + 0.3 × Experience
        
        Args:
            candidate: Candidate object
            job: Job object with requirements
            
        Returns:
            ScoreResult with rounded scores
        """
        # Calculate individual scores
        skill_result = SkillMatcher.match(candidate.skills, job.required_skills)
        experience_result = ExperienceMatcher.match(
            candidate.raw_text or "",
            job.minimum_experience
        )
        
        # Calculate final score with weights
        skill_score = round(skill_result.skill_score)
        experience_score = round(experience_result.experience_score)
        final_score = round(
            skill_score * Config.SKILL_WEIGHT +
            experience_score * Config.EXPERIENCE_WEIGHT
        )
        
        return ScoreResult(
            skill_result=skill_result,
            experience_result=experience_result,
            skill_score=skill_score,
            experience_score=experience_score,
            final_score=final_score
        )
