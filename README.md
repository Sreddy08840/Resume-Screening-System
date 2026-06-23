
# Resume Screening System

A professional, full-stack application to automate the resume screening process. Features a beautiful React + Tailwind CSS frontend and FastAPI backend!


## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Example Input](#example-input)
- [Example Output](#example-output)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Contributors](#contributors)


## Project Overview
The Resume Screening System is a powerful, extensible tool that parses, analyzes, and ranks candidate resumes against job requirements using modular architecture for efficient hiring processes.

**✨ Now with beautiful modern web UI! ✨**


## Features
### Core Capabilities
- **Multiple File Support**: Parse PDF, DOCX, and plain text (TXT) resume formats
- **Comprehensive Extraction**: Extract key information like name, email, phone, skills, experience, and education
- **Skill Matching**: Support exact and partial matching, ignoring case and duplicates
- **Experience Scoring**: Calculate experience score against minimum required experience
- **Final Scoring System**: Weighted final score (70% skill score, 30% experience score)
- **Recommendation Engine**: Categorize candidates as Highly Recommended, Recommended, Consider, or Reject
- **Reporting**: Generate both text and JSON reports
- **JSON Storage**: Save parsed resumes, job requirements, and reports

### Quality Features
- **Comprehensive Logging**: Logs to file and console
- **Robust Error Handling**: Doesn't crash on invalid/corrupted/empty/unsupported files
- **Modular Architecture**: Easy to extend and customize
- **Follow PEP 8 Standards**: Clean, maintainable code
- **Unit Tests**: 70%+ coverage of core components


## Folder Structure
```
resume-screening-system/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── parser/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── txt_parser.py
│   ├── text_cleaner.py
│   └── exceptions.py
├── matcher/
│   ├── __init__.py
│   ├── skill_matcher.py
│   ├── experience_matcher.py
│   ├── scoring.py
│   └── recommendation.py
├── reports/
│   ├── __init__.py
│   ├── json_handler.py
│   ├── report_generator.py
│   └── exceptions.py
├── utils/
│   ├── __init__.py
│   ├── extractor.py
│   ├── regex_patterns.py
│   └── file_utils.py
├── models/
│   ├── __init__.py
│   ├── candidate.py
│   └── job.py
├── data/
│   ├── resumes/
│   ├── jobs/
│   ├── parsed/
│   ├── reports/
│   └── logs/
└── tests/
```


## Installation

### Prerequisites
- Python 3.8+

### Steps
1. **Clone or download the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare folders** (data/ and subdirectories are already created)


## Usage

### 🖥️ Web Application (Recommended)
Run the beautiful web interface with React + FastAPI!

1. **Start the backend server**
   ```bash
   py -m uvicorn api:app --reload
   ```
   Backend will be at: http://localhost:8000
   API Documentation: http://localhost:8000/docs

2. **Open the frontend**
   Simply open `index.html` in your browser!


### 📟 Command Line Interface
Use the traditional command line interface as well:

1. **Prepare Job Requirements**
   Create a job requirements JSON file in `data/jobs/` (see the format below)

2. **Add Resumes**
   Place all resumes in `data/resumes/`

3. **Run the Application**
   ```bash
   py app.py
   ```

4. **Review Results**
   Check reports are in `data/reports/` and logs are in `data/logs/`


### 🚀 Quick Start Script!
For convenience, you can use the provided script:
```bash
py run_app.py
```


## Example Input

### Job Requirements
```json
{
  "title": "Python Developer",
  "location": "Remote",
  "description": "We are looking for an experienced Python developer",
  "required_skills": [
    "Python",
    "Django",
    "SQL",
    "PostgreSQL",
    "Git"
  ],
  "minimum_experience": 2
}
```

### Sample Resume
```
John Doe
john.doe@example.com
(555) 123-4567

Skills:
- Python
- Django
- SQL
- PostgreSQL
- Git
- Docker
- Flask
- AWS

Experience:
8 years of experience

Education:
Bachelor of Computer Science, University of Technology
```


## Example Output

### Console Output
```
================================================================================
RESUME SCREENING SYSTEM
================================================================================

Step 1: Loading job requirements...
==================================================
Job Requirements
==================================================
Title:       Python Developer
Location:    Remote

Required Skills:
  - Python
  - Django
  - SQL
  - PostgreSQL
  - Git

Minimum Experience: 2 years

Description: We are looking for an experienced Python developer
==================================================

Step 2: Parsing resumes...
Processed 3 files: 1 successful, 2 failed

Failed files:
  - empty.txt: Empty file
  - test.xyz: Unsupported file type

Step 3: Calculating recommendations...

Found 1 candidate(s):
================================================================================

Candidate #1: Highly Recommended
--------------------------------------------------------------------------------
==================================================
Candidate Information
==================================================
Name:        John Doe
Email:       john.doe@example.com

Skills:      Aws, Django, Docker, Flask, Git, Postgresql, Python, Sql
Experience:  8 years
Education:   Bachelor of Computer Science, University of Technology
==================================================

Score Breakdown:
  Skill Score: 100
  Experience Score: 100
  Final Score: 100
================================================================================

Step 4: Generating reports...
Text report saved to: E:\porjects\Resume Screening System\data\reports\screening_python_developer.txt
JSON report saved to: E:\porjects\Resume Screening System\data\reports\screening_python_developer.json

Text Report Preview:
================================================================================
================================================================================
RESUME SCREENING REPORT
================================================================================

JOB REQUIREMENTS
--------------------------------------------------------------------------------
Job Title: Python Developer
Location: Remote
Description: We are looking for an experienced Python developer
Required Skills: Python, Django, SQL, PostgreSQL, Git
Minimum Experience: 2 years

CANDIDATE RECOMMENDATIONS
--------------------------------------------------------------------------------

CANDIDATE #1: HIGHLY RECOMMENDED
================================================================================

CANDIDATE INFORMATION
----------------------------------------
Name: John Doe
Email: john.doe@example.com
Education: Bachelor of Computer Science, University of Technology

SKILLS
----------------------------------------
Matched Skills (5): Git, SQL, PostgreSQL, Python, Django
Missing Skills: None

EXPERIENCE
----------------------------------------
Candidate Experience: 8 years
Required Experience: 2 years
Experience Score: 100%

FINAL SCORE AND RECOMMENDATION
----------------------------------------
Skill Score: 100%
Experience Score: 100%
Final Score: 100%
Recommendation: Highly Recommended
================================================================================

================================================================================
END OF REPORT
================================================================================

================================================================================
PROCESS COMPLETED SUCCESSFULLY!
Log file: E:\porjects\Resume Screening System\data\logs\resume_screening.log
================================================================================
```


## Technologies Used
### Backend
- **Python 3.x**: 3.8+
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **PDF Parsing**: PyPDF2, pdfplumber
- **DOCX Parsing**: python-docx
- **Testing**: pytest, pytest-cov

### Frontend
- **React 18**: Modern UI library
- **Tailwind CSS**: Beautiful styling
- **Font Awesome**: Icons
- **CDN Delivery**: No build process needed

### General
- **PEP8 Compliance**: Code follows Python's style guide
- **Modular Architecture**: Clean, maintainable code


## Future Improvements
- [ ] NLP-based extractor for better information extraction
- [ ] Web interface for easy usage
- [ ] Database integration for persistent data
- [ ] Advanced report visualization using matplotlib/seaborn
- [ ] Resume ranker with configurable weights
- [ ] Support for more file formats (RTF, HTML, etc.)
- [ ] Resume ranking with fuzzy logic matching
- [ ] Batch processing with queue system


## License
This project is for demonstration purposes. Please feel free to use and modify as needed.


## Contributors
Thanks to everyone who has contributed to this project!

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Sreddy08840">
        <img src="https://github.com/Sreddy08840.png" width="100px;" alt="Sreddy08840"/><br />
        <sub><b>Sreddy08840</b></sub>
      </a><br />
      <sub>🏗️ Architect · 🤖 AI Pipeline · 💻 Full Stack · 🚀 DevOps</sub>
    </td>
    <!-- Add new contributors below -->
  </tr>
</table>

> Want your name here? Check the [Contributing Guide](#-contributing) and submit a PR!

---
