
from typing import List, Dict, Optional, Any
import re
from utils.regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    YEARS_EXPERIENCE_PATTERN,
    SKILLS_HEADERS,
    EXPERIENCE_HEADERS,
    EDUCATION_HEADERS,
    COMMON_SKILLS
)


class CandidateExtractor:
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        return EMAIL_PATTERN.findall(text)
    
    @staticmethod
    def extract_phones(text: str) -> List[str]:
        return PHONE_PATTERN.findall(text)
    
    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        lines = text.strip().split('\n')
        
        # Try to find name in first few lines
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            # Skip lines with emails or phones
            if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line):
                continue
            
            # Check for 2-3 word lines that look like names
            words = line.split()
            if 2 <= len(words) <= 4 and all(w.istitle() or w.isupper() for w in words if w.isalpha()):
                return ' '.join(w.title() for w in words)
        
        return None
    
    @staticmethod
    def extract_years_experience(text: str) -> int:
        matches = YEARS_EXPERIENCE_PATTERN.findall(text)
        if matches:
            return max(int(m) for m in matches)
        return 0
    
    @staticmethod
    def extract_section(text: str, header_pattern: re.Pattern) -> List[str]:
        lines = text.split('\n')
        in_section = False
        section_content = []
        
        for line in lines:
            line_clean = line.strip().lower()
            
            if header_pattern.search(line_clean):
                in_section = True
                continue
            
            if in_section:
                # Check if we hit another section header
                if any(p.search(line_clean) for p in [SKILLS_HEADERS, EXPERIENCE_HEADERS, EDUCATION_HEADERS]):
                    break
                if line.strip():
                    section_content.append(line.strip())
        
        return section_content
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        skills = set()
        text_lower = text.lower()
        
        # Try to extract from skills section
        skills_section = CandidateExtractor.extract_section(text, SKILLS_HEADERS)
        for line in skills_section:
            # Split by common separators
            items = re.split(r'[,;•/|]', line)
            for item in items:
                item = item.strip()
                item = re.sub(r'^[-\s*]+|[-\s*]+$', '', item)
                if item:
                    skills.add(item.lower())
        
        # Also match against common skills list
        for skill in COMMON_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                skills.add(skill.lower())
        
        # Normalize to title case
        return sorted([skill.title() for skill in skills])
    
    @staticmethod
    def extract_education(text: str) -> str:
        education_section = CandidateExtractor.extract_section(text, EDUCATION_HEADERS)
        if education_section:
            return ' '.join(education_section)
        return ''
    
    @staticmethod
    def extract_all(text: str) -> Dict[str, Any]:
        emails = CandidateExtractor.extract_emails(text)
        phones = CandidateExtractor.extract_phones(text)
        
        return {
            'name': CandidateExtractor.extract_name(text) or '',
            'email': emails[0] if emails else '',
            'phone': phones[0] if phones else '',
            'skills': CandidateExtractor.extract_skills(text),
            'experience': CandidateExtractor.extract_years_experience(text),
            'education': CandidateExtractor.extract_education(text)
        }
