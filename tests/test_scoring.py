
import pytest
from models.candidate import Candidate
from models.job import Job
from matcher.scoring import Scorer


class TestScoring:
    """Test suite for Scorer class."""

    def test_calculate_score_full_marks(self):
        """Test when candidate gets full score."""
        candidate = Candidate(
            name="Test",
            skills=["Python", "Django", "SQL", "PostgreSQL", "Git"],
            raw_text="8 years of experience"
        )
        job = Job(
            title="Python Dev",
            required_skills=["Python", "Django", "SQL", "PostgreSQL", "Git"],
            minimum_experience=2
        )
        
        result = Scorer.calculate_score(candidate, job)
        
        assert result.skill_score == 100
        assert result.experience_score == 100
        assert result.final_score == 100

    def test_calculate_score_weighted(self):
        """Test weighted scoring calculation."""
        # 70% skill score, 30% experience score
        candidate = Candidate(
            name="Test",
            skills=["Python", "Django"],  # 2/5 skills
            raw_text="1 year of experience"  # 1/2 years
        )
        job = Job(
            title="Python Dev",
            required_skills=["Python", "Django", "SQL", "PostgreSQL", "Git"],
            minimum_experience=2
        )
        
        result = Scorer.calculate_score(candidate, job)
        
        # 40 * 0.7 + 50 * 0.3 = 28 + 15 = 43
        assert result.final_score == 43

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        candidate = Candidate(name="Test", skills=["Python"], raw_text="2 years")
        job = Job(title="Dev", required_skills=["Python"], minimum_experience=2)
        
        result = Scorer.calculate_score(candidate, job)
        result_dict = result.to_dict()
        
        assert "skill_result" in result_dict
        assert "experience_result" in result_dict
        assert "skill_score" in result_dict
        assert "experience_score" in result_dict
        assert "final_score" in result_dict

