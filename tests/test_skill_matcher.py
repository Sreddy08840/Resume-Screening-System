
import pytest
from matcher.skill_matcher import SkillMatcher


class TestSkillMatcher:
    """Test suite for SkillMatcher class."""

    def test_match_all_skills(self):
        """Test when all skills match."""
        candidate_skills = ["Python", "Django", "SQL"]
        required_skills = ["Python", "Django", "SQL"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert set(result.matched_skills) == set(required_skills)
        assert result.missing_skills == []
        assert result.skill_percentage == 100.0
        assert result.skill_score == 100.0

    def test_match_partial_skills(self):
        """Test when some skills match."""
        candidate_skills = ["Python", "SQL"]
        required_skills = ["Python", "Django", "SQL"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert "Python" in result.matched_skills
        assert "SQL" in result.matched_skills
        assert "Django" in result.missing_skills
        assert round(result.skill_percentage) == 67
        assert result.skill_score == 66.67

    def test_no_matching_skills(self):
        """Test when no skills match."""
        candidate_skills = ["Java", "C++"]
        required_skills = ["Python", "Django", "SQL"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert result.matched_skills == []
        assert len(result.missing_skills) == 3
        assert result.skill_percentage == 0.0
        assert result.skill_score == 0.0

    def test_case_insensitive_matching(self):
        """Test that matching is case insensitive."""
        candidate_skills = ["python", "django", "sql"]
        required_skills = ["Python", "Django", "SQL"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert result.skill_percentage == 100.0

    def test_duplicate_skills_ignored(self):
        """Test that duplicate candidate skills are ignored."""
        candidate_skills = ["Python", "Python", "Django", "Django"]
        required_skills = ["Python", "Django"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert len(result.matched_skills) == 2
        assert result.skill_percentage == 100.0

    def test_partial_matching(self):
        """Test partial skill matching."""
        candidate_skills = ["Python3", "Django Rest"]
        required_skills = ["Python", "Django"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        # Should match partially
        assert len(result.matched_skills) == 2

    def test_empty_candidate_skills(self):
        """Test when candidate has no skills."""
        candidate_skills = []
        required_skills = ["Python", "Django"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert result.skill_percentage == 0.0

    def test_empty_required_skills(self):
        """Test when no skills are required."""
        candidate_skills = ["Python"]
        required_skills = []
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        
        assert result.skill_percentage == 100.0

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        candidate_skills = ["Python", "Django"]
        required_skills = ["Python", "Django"]
        
        result = SkillMatcher.match(candidate_skills, required_skills)
        result_dict = result.to_dict()
        
        assert "matched_skills" in result_dict
        assert "missing_skills" in result_dict
        assert "skill_percentage" in result_dict
        assert "skill_score" in result_dict

