
"""Candidate recommendation engine that sorts candidates by score."""
from typing import List, Dict, Any
from models.candidate import Candidate
from models.job import Job
from matcher.scoring import Scorer, ScoreResult
from config import Config


class Recommendation:
    """
    Complete recommendation for a single candidate.

    Attributes:
        candidate: Candidate object.
        score_result: Detailed scoring data.
        recommendation: Recommendation string (Highly Recommended, etc.).
    """

    def __init__(self, candidate: Candidate, score_result: ScoreResult) -> None:
        self.candidate = candidate
        self.score_result = score_result
        self.recommendation = self._get_recommendation_string()

    def _get_recommendation_string(self) -> str:
        """
        Determines recommendation category based on final score.

        Categories:
            - 85-100: Highly Recommended
            - 70-84: Recommended
            - 50-69: Consider
            - Below 50: Reject

        Returns:
            Recommendation string.
        """
        score = self.score_result.final_score
        if 85 <= score <= 100:
            return "Highly Recommended"
        elif 70 <= score <= 84:
            return "Recommended"
        elif 50 <= score <= 69:
            return "Consider"
        else:
            return "Reject"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts recommendation to a dictionary for serialization.

        Returns:
            Dictionary representation of the recommendation.
        """
        return {
            "candidate": self.candidate.to_dict(),
            "score_result": self.score_result.to_dict(),
            "recommendation": self.recommendation,
        }


class Recommender:
    """Generates sorted candidate recommendations for a job."""

    @staticmethod
    def recommend(candidates: List[Candidate], job: Job) -> List[Recommendation]:
        """
        Scores and ranks candidates for a job.

        Args:
            candidates: List of Candidate objects.
            job: Job requirements.

        Returns:
            List of Recommendation objects sorted by final score descending.
        """
        recommendations = []
        for candidate in candidates:
            score_result = Scorer.calculate_score(candidate, job)
            recommendation = Recommendation(candidate, score_result)
            recommendations.append(recommendation)

        # Sort by final score descending
        recommendations.sort(key=lambda x: x.score_result.final_score, reverse=True)

        return recommendations
