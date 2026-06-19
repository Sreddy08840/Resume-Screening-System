
import os
from config import Config
from models.candidate import Candidate
from models.job import Job
from reports.json_handler import JSONHandler


def test_json_handler():
    print("=" * 60)
    print("Testing JSON Handler")
    print("=" * 60)
    
    # Test 1: Save and load a candidate
    print("\nTest 1: Saving and loading candidate")
    candidate = Candidate(
        name="Test Candidate",
        email="test@example.com",
        phone="123-456-7890",
        skills=["Python", "Django"],
        experience=5,
        education="Bachelor's Degree"
    )
    saved_path = JSONHandler.save_parsed_candidate(candidate)
    print(f"Saved candidate to: {saved_path}")
    
    loaded_candidate = JSONHandler.load_parsed_candidate(saved_path)
    assert loaded_candidate.name == candidate.name, "Name mismatch!"
    assert loaded_candidate.email == candidate.email, "Email mismatch!"
    print("Candidate loaded successfully!")
    
    # Test 2: Save and load a report
    print("\nTest 2: Saving and loading report")
    test_report = {
        "job_title": "Test Job",
        "total_candidates": 1,
        "recommendations": [candidate.to_dict()]
    }
    report_path = JSONHandler.save_analysis_report(test_report, "test_report.json")
    print(f"Saved report to: {report_path}")
    
    reports = JSONHandler.load_reports()
    print(f"Loaded {len(reports)} report(s)!")
    
    # Test 3: Pretty print
    print("\nTest 3: Pretty print JSON")
    pretty_json = JSONHandler._pretty_print_json(candidate.to_dict())
    print("Pretty-printed candidate data:")
    print(pretty_json)
    
    # Clean up test files
    os.remove(saved_path)
    os.remove(report_path)
    print("\nTest files cleaned up!")
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_json_handler()
