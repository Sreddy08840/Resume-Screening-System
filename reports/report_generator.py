
"""Generates both text and JSON reports for resume screening results."""
import json
import os
from typing import List, Dict, Any, Optional
from config import Config
from utils.file_utils import ensure_dir
from models.candidate import Candidate
from models.job import Job
from matcher.recommendation import Recommendation


class ReportGenerator:
    """
    Generates professional reports for resume screening results.
    Supports both plain text and JSON formats.
    """

    @staticmethod
    def _generate_text_report(job: Job, recommendations: List[Recommendation]) -> str:
        """
        Generates a human-readable text report.

        Args:
            job: Job requirements.
            recommendations: List of candidate recommendations.

        Returns:
            Formatted text report string.
        """
        lines = []
        lines.append("=" * 80)
        lines.append("RESUME SCREENING REPORT")
        lines.append("=" * 80)
        lines.append("\nJOB REQUIREMENTS")
        lines.append("-" * 80)
        lines.append(f"Job Title: {job.title}")
        if job.location:
            lines.append(f"Location: {job.location}")
        if job.description:
            lines.append(f"Description: {job.description}")
        lines.append(f"Required Skills: {', '.join(job.required_skills)}")
        lines.append(f"Minimum Experience: {job.minimum_experience} years")

        lines.append("\nCANDIDATE RECOMMENDATIONS")
        lines.append("-" * 80)

        if not recommendations:
            lines.append("No candidates found meeting the minimum requirements.")
        else:
            for i, rec in enumerate(recommendations, 1):
                candidate = rec.candidate
                score_result = rec.score_result

                lines.append(f"\nCANDIDATE #{i}: {rec.recommendation.upper()}")
                lines.append("=" * 80)
                lines.append("\nCANDIDATE INFORMATION")
                lines.append("-" * 40)
                if candidate.name:
                    lines.append(f"Name: {candidate.name}")
                if candidate.email:
                    lines.append(f"Email: {candidate.email}")
                if candidate.phone:
                    lines.append(f"Phone: {candidate.phone}")
                if candidate.education:
                    lines.append(f"Education: {candidate.education}")

                lines.append("\nSKILLS")
                lines.append("-" * 40)
                matched = score_result.skill_result.matched_skills
                if matched:
                    lines.append(f"Matched Skills ({len(matched)}): {', '.join(matched)}")
                else:
                    lines.append("Matched Skills: None")

                missing = score_result.skill_result.missing_skills
                if missing:
                    lines.append(f"Missing Skills ({len(missing)}): {', '.join(missing)}")
                else:
                    lines.append("Missing Skills: None")

                lines.append("\nEXPERIENCE")
                lines.append("-" * 40)
                lines.append(
                    f"Candidate Experience: {score_result.experience_result.candidate_years} years"
                )
                lines.append(f"Required Experience: {job.minimum_experience} years")
                lines.append(f"Experience Score: {score_result.experience_score}%")

                lines.append("\nFINAL SCORE AND RECOMMENDATION")
                lines.append("-" * 40)
                lines.append(f"Skill Score: {score_result.skill_score}%")
                lines.append(f"Experience Score: {score_result.experience_score}%")
                lines.append(f"Final Score: {score_result.final_score}%")
                lines.append(f"Recommendation: {rec.recommendation}")
                lines.append("=" * 80)

        lines.append("\n" + "=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def _generate_json_report_data(
        job: Job, recommendations: List[Recommendation]
    ) -> Dict[str, Any]:
        """
        Generates structured JSON report data.

        Args:
            job: Job requirements.
            recommendations: List of candidate recommendations.

        Returns:
            Dictionary with all report data for serialization.
        """
        rec_dicts = [rec.to_dict() for rec in recommendations]
        return {
            "job_title": job.title,
            "job_location": job.location,
            "job_description": job.description,
            "required_skills": job.required_skills,
            "minimum_experience": job.minimum_experience,
            "total_candidates": len(recommendations),
            "recommendations": rec_dicts,
        }

    @staticmethod
    def generate_reports(
        job: Job,
        recommendations: List[Recommendation],
        base_filename: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generates both text and JSON reports and saves them to disk.

        Args:
            job: Job requirements.
            recommendations: List of candidate recommendations.
            base_filename: Optional base filename (without extension).

        Returns:
            Dictionary with paths to the generated text and JSON reports.
        """
        ensure_dir(Config.REPORTS_DIR)

        if not base_filename:
            base_filename = f"report_{job.title.replace(' ', '_').lower()}"

        # Generate and save text report
        text_filename = f"{base_filename}.txt"
        text_filepath = os.path.join(Config.REPORTS_DIR, text_filename)
        text_content = ReportGenerator._generate_text_report(job, recommendations)
        with open(text_filepath, "w", encoding="utf-8") as f:
            f.write(text_content)

        # Generate and save JSON report
        json_filename = f"{base_filename}.json"
        json_filepath = os.path.join(Config.REPORTS_DIR, json_filename)
        json_data = ReportGenerator._generate_json_report_data(job, recommendations)
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        return {
            "text_report": text_filepath,
            "json_report": json_filepath,
        }
