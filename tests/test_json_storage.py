
import os
import json
import pytest
from reports.json_handler import JSONHandler
from models.candidate import Candidate
from models.job import Job
from reports.exceptions import InvalidJSONError, MissingRequiredFieldError


class TestJSONStorage:
    """Test suite for JSONHandler class."""

    def test_save_and_load_candidate(self, test_data_dir):
        """Test saving and loading a candidate."""
        candidate = Candidate(
            name="John Doe",
            email="john@example.com",
            phone="555-1234",
            skills=["Python", "Django"],
            experience=5,
            education="BS CS"
        )
        
        # Temporarily change PARSED_DIR for testing
        original_parsed_dir = Config.PARSED_DIR
        Config.PARSED_DIR = os.path.join(test_data_dir, "parsed")
        
        try:
            saved_path = JSONHandler.save_parsed_candidate(candidate, "test_candidate.json")
            loaded_candidate = JSONHandler.load_parsed_candidate(saved_path)
            
            assert loaded_candidate.name == candidate.name
            assert loaded_candidate.email == candidate.email
            assert set(loaded_candidate.skills) == set(candidate.skills)
        finally:
            Config.PARSED_DIR = original_parsed_dir

    def test_load_job_valid(self, test_data_dir, sample_job_requirements):
        """Test loading a valid job from JSON."""
        job_path = os.path.join(test_data_dir, "jobs", "test_job.json")
        with open(job_path, "w", encoding="utf-8") as f:
            json.dump(sample_job_requirements, f)
        
        job = JSONHandler.load_job(job_path)
        
        assert job.title == sample_job_requirements["title"]
        assert job.required_skills == sample_job_requirements["required_skills"]
        assert job.minimum_experience == sample_job_requirements["minimum_experience"]

    def test_load_job_missing_required_fields(self, test_data_dir):
        """Test loading a job with missing required fields raises error."""
        job_data = {"title": "Missing Fields"}
        job_path = os.path.join(test_data_dir, "jobs", "invalid_job.json")
        with open(job_path, "w", encoding="utf-8") as f:
            json.dump(job_data, f)
        
        with pytest.raises(MissingRequiredFieldError):
            JSONHandler.load_job(job_path)

    def test_load_invalid_json(self, test_data_dir):
        """Test loading invalid JSON file."""
        job_path = os.path.join(test_data_dir, "jobs", "invalid_json.txt")
        with open(job_path, "w", encoding="utf-8") as f:
            f.write("invalid json content here")
        
        with pytest.raises(InvalidJSONError):
            JSONHandler.load_job(job_path)

    def test_save_and_load_reports(self, test_data_dir):
        """Test saving and loading reports."""
        original_reports_dir = Config.REPORTS_DIR
        Config.REPORTS_DIR = os.path.join(test_data_dir, "reports")
        
        try:
            report_data = {"test": "data"}
            saved_path = JSONHandler.save_analysis_report(report_data, "test_report.json")
            
            reports = JSONHandler.load_reports()
            assert len(reports) >= 1
        finally:
            Config.REPORTS_DIR = original_reports_dir


from config import Config

