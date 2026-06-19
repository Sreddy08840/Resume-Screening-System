
"""Job requirements data model and validation logic."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Job:
    """
    Data model representing job requirements for a position.

    Attributes:
        title: Job title.
        description: Job description.
        required_skills: List of skills required for the job.
        minimum_experience: Minimum years of experience required.
        location: Job location.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = field(default_factory=list)
    minimum_experience: int = 0
    location: Optional[str] = None

    def __post_init__(self) -> None:
        """Validates job data after initialization."""
        self.validate()

    def validate(self) -> List[str]:
        """
        Validates the job requirements data.

        Returns:
            List of validation error messages (empty if valid).
        """
        errors = []

        if not self.title or len(self.title.strip()) == 0:
            errors.append("Job title is required")

        if self.minimum_experience < 0:
            errors.append("Minimum experience cannot be negative")

        return errors

    def is_valid(self) -> bool:
        """
        Checks if job data is valid.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate()) == 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts job object to a dictionary.

        Returns:
            Dictionary representation of the job.
        """
        return {
            "title": self.title,
            "description": self.description,
            "required_skills": self.required_skills,
            "minimum_experience": self.minimum_experience,
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Job":
        """
        Creates a Job object from a dictionary.

        Args:
            data: Dictionary with job data.

        Returns:
            Job instance.
        """
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            required_skills=data.get("required_skills", []),
            minimum_experience=data.get("minimum_experience", 0),
            location=data.get("location"),
        )

    def pretty_print(self) -> str:
        """
        Returns a formatted string representation of the job requirements.

        Returns:
            Pretty-printed job information.
        """
        lines = []
        lines.append("=" * 50)
        lines.append("Job Requirements")
        lines.append("=" * 50)

        if self.title:
            lines.append(f"Title:       {self.title}")
        if self.location:
            lines.append(f"Location:    {self.location}")

        if self.required_skills:
            lines.append(f"\nRequired Skills:")
            for skill in self.required_skills:
                lines.append(f"  • {skill}")

        lines.append(f"\nMinimum Experience: {self.minimum_experience} years")

        if self.description:
            lines.append(f"\nDescription: {self.description}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def __str__(self) -> str:
        """Returns string representation of the job."""
        return self.pretty_print()
