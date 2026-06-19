import re

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b')
YEARS_EXPERIENCE_PATTERN = re.compile(r'(?:^|(?<![.\d]))(\d+)\s*\+?\s*(?:years|year)', re.IGNORECASE)

# Section headers patterns
SKILLS_HEADERS = re.compile(r'\b(skills|technical skills|core competencies|key skills|skills & expertise)\b', re.IGNORECASE)
EXPERIENCE_HEADERS = re.compile(r'\b(experience|work experience|employment history|professional experience)\b', re.IGNORECASE)
EDUCATION_HEADERS = re.compile(r'\b(education|academic background|qualifications|degrees)\b', re.IGNORECASE)

# Common technical skills (for demonstration)
COMMON_SKILLS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust',
    'django', 'flask', 'spring', 'react', 'angular', 'vue', 'node.js',
    'sql', 'postgresql', 'mysql', 'mongodb', 'oracle', 'nosql',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
    'machine learning', 'deep learning', 'nlp', 'data science',
    'html', 'css', 'typescript', 'api', 'rest', 'graphql'
]
