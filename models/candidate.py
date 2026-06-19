
"""Candidate data model and validation logic."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import re


@dataclass
class Candidate:
    """
    Data model representing a job candidate with extracted information.

    Attributes:
        name: Candidate's full name.
        email: Candidate's email address.
        phone: Candidate's phone number.
        skills: List of candidate's skills.
        experience: Number of years of experience.
        education: Candidate's education background.
        raw_text: Original text from resume.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience: int = 0
    education: str = ""
    raw_text: Optional[str] = None

    EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def __post_init__(self) -> None:
        """Validates candidate data after initialization."""
        self.validate()

    def validate(self) -> List[str]:
        """
        Validates the candidate data.

        Returns:
            List of validation error messages (empty if valid).
        """
        errors = []

        if self.name is not None and len(self.name.strip()) == 0:
            errors.append("Name cannot be empty")

        if self.email is not None and self.email.strip() != "":
            if not self.EMAIL_REGEX.match(self.email):
                errors.append(f"Invalid email format: {self.email}")

        if self.experience < 0:
            errors.append("Experience years cannot be negative")

        return errors

    def is_valid(self) -> bool:
        """
        Checks if candidate data is valid.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate()) == 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts candidate object to a dictionary.

        Returns:
            Dictionary representation of the candidate.
        """
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candidate":
        """
        Creates a Candidate object from a dictionary.

        Args:
            data: Dictionary with candidate data.

        Returns:
            Candidate instance.
        """
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            skills=data.get("skills", []),
            experience=data.get("experience", 0),
            education=data.get("education", ""),
        )

    def pretty_print(self) -> str:
        """
        Returns a formatted string representation of the candidate.

        Returns:
            Pretty-printed candidate information.
        """
        lines = []
        lines.append("=" * 50)
        lines.append("Candidate Information")
        lines.append("=" * 50)

        if self.name:
            lines.append(f"Name:        {self.name}")
        if self.email:
            lines.append(f"Email:       {self.email}")
        if self.phone:
            lines.append(f"Phone:       {self.phone}")

        if self.skills:
            lines.append(f"\nSkills:      {', '.join(self.skills)}")

        lines.append(f"Experience:  {self.experience} years")

        if self.education:
            lines.append(f"Education:   {self.education}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def __str__(self) -> str:
        """Returns string representation of the candidate."""
        return self.pretty_print()
