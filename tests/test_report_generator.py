
import os
import pytest
from reports.report_generator import ReportGenerator
from models.candidate import Candidate
from models.job import Job
from matcher.recommendation import Recommendation
from matcher.scoring import Scorer


class TestReportGenerator:
    """Test suite for ReportGenerator class."""

    def test_generate_text_report(self, test_data_dir):
        """Test generating text report."""
        candidate = Candidate(
            name="John Doe",
            email="john@example.com",
            phone="555-1234",
            skills=["Python", "Django", "SQL"],
            raw_text="8 years of experience"
        )
        job = Job(
            title="Python Developer",
            required_skills=["Python", "Django", "SQL", "Git"],
            minimum_experience=2
        )
        
        score_result = Scorer.calculate_score(candidate, job)
        recommendation = Recommendation(candidate, score_result)
        
        text_report = ReportGenerator._generate_text_report(job, [recommendation])
        
        assert "John Doe" in text_report
        assert "Python" in text_report

    def test_generate_json_report_data(self, test_data_dir):
        """Test generating JSON report data."""
        candidate = Candidate(name="John Doe", skills=["Python"], raw_text="3 years")
        job = Job(title="Python Dev", required_skills=["Python"], minimum_experience=2)
        
        score_result = Scorer.calculate_score(candidate, job)
        recommendation = Recommendation(candidate, score_result)
        
        json_data = ReportGenerator._generate_json_report_data(job, [recommendation])
        
        assert "job_title" in json_data
        assert "required_skills" in json_data
        assert "recommendations" in json_data
        assert len(json_data["recommendations"]) == 1

    def test_generate_reports(self, test_data_dir):
        """Test generating both text and JSON reports."""
        original_reports_dir = Config.REPORTS_DIR
        Config.REPORTS_DIR = os.path.join(test_data_dir, "reports")
        
        try:
            candidate = Candidate(
                name="John Doe",
                skills=["Python", "Django"],
                raw_text="5 years"
            )
            job = Job(
                title="Python Dev",
                required_skills=["Python", "Django"],
                minimum_experience=2
            )
            
            score_result = Scorer.calculate_score(candidate, job)
            recommendation = Recommendation(candidate, score_result)
            
            report_paths = ReportGenerator.generate_reports(
                job, [recommendation], "test_report"
            )
            
            assert os.path.exists(report_paths["text_report"])
            assert os.path.exists(report_paths["json_report"])
        finally:
            Config.REPORTS_DIR = original_reports_dir


from config import Config

