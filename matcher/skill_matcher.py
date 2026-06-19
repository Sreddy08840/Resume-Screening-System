
from typing import List, Dict, Any, Set
import re


class SkillMatchResult:
    def __init__(self):
        self.matched_skills: List[str] = []
        self.missing_skills: List[str] = []
        self.skill_percentage: float = 0.0
        self.skill_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'skill_percentage': self.skill_percentage,
            'skill_score': self.skill_score
        }


class SkillMatcher:
    @staticmethod
    def _normalize_skills(skills: List[str]) -> Set[str]:
        """Normalize skills: lowercase, remove duplicates, trim whitespace"""
        normalized = set()
        for skill in skills:
            if skill:
                normalized.add(skill.strip().lower())
        return normalized
    
    @staticmethod
    def _is_partial_match(required_skill: str, candidate_skill: str) -> bool:
        """Check if required skill is a substring of candidate skill or vice versa"""
        req = required_skill.lower()
        cand = candidate_skill.lower()
        return req in cand or cand in req
    
    @staticmethod
    def match(
        candidate_skills: List[str], 
        required_skills: List[str],
        partial_match: bool = True
    ) -> SkillMatchResult:
        """
        Match candidate skills with required skills
        
        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills
            partial_match: Whether to allow partial matching (substring matches)
            
        Returns:
            SkillMatchResult with matched skills, missing skills, percentage, and score
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
            
            if found:
                matched_count += 1
                # Find original case version for display
                original_req = next(
                    (s for s in required_skills if s.lower() == req_skill),
                    req_skill.title()
                )
                result.matched_skills.append(original_req)
            else:
                # Find original case version
                original_req = next(
                    (s for s in required_skills if s.lower() == req_skill),
                    req_skill.title()
                )
                result.missing_skills.append(original_req)
        
        # Calculate percentage and score
        total_required = len(required_skills_normalized)
        result.skill_percentage = (matched_count / total_required) * 100
        result.skill_score = round(result.skill_percentage, 2)
        
        return result

