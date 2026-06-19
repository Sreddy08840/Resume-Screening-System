
import os
import tempfile
import shutil
import pytest
from config import Config


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary test data directory."""
    test_dir = tempfile.mkdtemp(prefix="resume_test_")
    
    # Create subdirectories
    os.makedirs(os.path.join(test_dir, "resumes"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "jobs"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "parsed"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "reports"), exist_ok=True)
    
    yield test_dir
    
    # Cleanup
    shutil.rmtree(test_dir)


@pytest.fixture
def sample_resume_content():
    """Return sample resume text for testing."""
    return """John Doe
john.doe@example.com
(555) 123-4567

Skills: Python, Django, SQL, PostgreSQL, Git, Docker, Flask, AWS

Experience: 8 years

Education: Bachelor of Computer Science, University of Technology
"""


@pytest.fixture
def sample_job_requirements():
    """Return sample job requirements for testing."""
    return {
        "title": "Python Developer",
        "required_skills": ["Python", "Django", "SQL", "PostgreSQL", "Git"],
        "minimum_experience": 2,
        "location": "Remote",
        "description": "Looking for a Python developer"
    }

