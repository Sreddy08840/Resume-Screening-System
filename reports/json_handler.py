
"""Handles JSON serialization/deserialization of candidate and job data."""
import json
import os
from typing import Dict, Any, List, Optional
from models.candidate import Candidate
from models.job import Job
from config import logger, Config
from utils.file_utils import ensure_dir
from reports.exceptions import (
    JobLoaderError,
    InvalidJSONError,
    MissingRequiredFieldError,
    InvalidJobDataError,
)


class JSONHandler:
    """
    Utility for saving and loading JSON data for the resume screening system.
    Handles candidates, job requirements, and analysis reports.
    """

    @staticmethod
    def _pretty_print_json(data: Any) -> str:
        """
        Formats data as a pretty-printed JSON string.

        Args:
            data: Any JSON-serializable data.

        Returns:
            Formatted JSON string.
        """
        return json.dumps(data, indent=4, ensure_ascii=False)

    @staticmethod
    def save_parsed_candidate(
        candidate: Candidate, filename: Optional[str] = None
    ) -> str:
        """
        Saves a parsed candidate to a JSON file.

        Args:
            candidate: Candidate object to save.
            filename: Optional filename (uses candidate name if not provided).

        Returns:
            Full path to the saved file.
        """
        ensure_dir(Config.PARSED_DIR)

        if not filename:
            if candidate.name:
                safe_name = "".join(
                    c for c in candidate.name if c.isalnum() or c in (" ", "-", "_")
                ).rstrip()
                filename = f"parsed_{safe_name.replace(' ', '_')}.json"
            else:
                filename = "parsed_candidate.json"

        filepath = os.path.join(Config.PARSED_DIR, filename)

        try:
            data = candidate.to_dict()
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved parsed candidate to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save candidate: {e}", exc_info=True)
            raise JobLoaderError(f"Failed to save candidate: {str(e)}") from e

    @staticmethod
    def load_parsed_candidate(filepath: str) -> Candidate:
        """
        Loads a parsed candidate from a JSON file.

        Args:
            filepath: Path to the candidate JSON file.

        Returns:
            Candidate object.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Candidate file not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            candidate = Candidate.from_dict(data)
            logger.info(f"Loaded parsed candidate from: {filepath}")
            return candidate
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in candidate file: {e}")
            raise InvalidJSONError(f"Invalid JSON in candidate file: {str(e)}") from e
        except Exception as e:
            logger.error(f"Failed to load candidate: {e}", exc_info=True)
            raise JobLoaderError(f"Failed to load candidate: {str(e)}") from e

    @staticmethod
    def save_analysis_report(report_data: Dict[str, Any], filename: str) -> str:
        """
        Saves an analysis report to a JSON file.

        Args:
            report_data: Dictionary containing report data.
            filename: Name of the output file.

        Returns:
            Full path to the saved report.
        """
        ensure_dir(Config.REPORTS_DIR)
        filepath = os.path.join(Config.REPORTS_DIR, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved analysis report to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save report: {e}", exc_info=True)
            raise JobLoaderError(f"Failed to save report: {str(e)}") from e

    @staticmethod
    def load_reports() -> List[Dict[str, Any]]:
        """
        Loads all analysis reports from the reports directory.

        Returns:
            List of report data dictionaries.
        """
        reports = []
        ensure_dir(Config.REPORTS_DIR)

        for filename in os.listdir(Config.REPORTS_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(Config.REPORTS_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        reports.append(data)
                except Exception as e:
                    logger.warning(f"Failed to load report {filename}: {e}")

        logger.info(f"Loaded {len(reports)} reports")
        return reports

    @staticmethod
    def load_job(file_path: str) -> Job:
        """
        Loads job requirements from a JSON file and validates it.

        Args:
            file_path: Path to the job JSON file.

        Returns:
            Validated Job object.

        Raises:
            FileNotFoundError: If file doesn't exist.
            InvalidJSONError: If JSON is invalid.
            MissingRequiredFieldError: If required fields are missing.
            InvalidJobDataError: If job data fails validation.
        """
        if not os.path.exists(file_path):
            logger.error(f"Job file not found: {file_path}")
            raise FileNotFoundError(f"Job file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in job file: {e}")
            raise InvalidJSONError(f"Invalid JSON in {file_path}: {str(e)}") from e
        except Exception as e:
            logger.error(f"Error reading job file: {e}", exc_info=True)
            raise JobLoaderError(f"Error reading {file_path}: {str(e)}") from e

        # Validate required fields
        required_fields = ["title", "required_skills", "minimum_experience"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required fields in job file: {missing_fields}")
            raise MissingRequiredFieldError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            job = Job.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to create Job object: {e}", exc_info=True)
            raise InvalidJobDataError(f"Failed to create Job object: {str(e)}") from e

        # Validate job data
        validation_errors = job.validate()
        if validation_errors:
            logger.error(f"Invalid job data: {validation_errors}")
            raise InvalidJobDataError(
                f"Invalid job data: {', '.join(validation_errors)}"
            )

        logger.info(f"Successfully loaded job: {job.title}")
        return job

    @staticmethod
    def save_job(job: Job, file_path: str) -> None:
        """
        Saves job requirements to a JSON file.

        Args:
            job: Job object to save.
            file_path: Path to save the file.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(job.to_dict(), f, indent=4, ensure_ascii=False)
            logger.info(f"Saved job to: {file_path}")
        except Exception as e:
            logger.error(f"Error saving job: {e}", exc_info=True)
            raise JobLoaderError(f"Error saving to {file_path}: {str(e)}") from e
