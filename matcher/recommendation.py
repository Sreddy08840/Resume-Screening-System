
from typing import List, Dict, Any
from models.candidate import Candidate
from models.job import Job
from matcher.scoring import Scorer, ScoreResult
from config import Config


class Recommendation:
    def __init__(self, candidate: Candidate, score_result: ScoreResult):
        self.candidate = candidate
        self.score_result = score_result
        self.recommendation = self._get_recommendation_string()
    
    def _get_recommendation_string(self) -> str:
        """
        Get recommendation string based on final score:
        85-100 → Highly Recommended
        70-84 → Recommended
        50-69 → Consider
        Below 50 → Reject
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
        return {
            "candidate": self.candidate.to_dict(),
            "score_result": self.score_result.to_dict(),
            "recommendation": self.recommendation
        }


class Recommender:
    @staticmethod
    def recommend(candidates: List[Candidate], job: Job) -> List[Recommendation]:
        """
        Recommend candidates for a job
        
        Args:
            candidates: List of Candidate objects
            job: Job object with requirements
            
        Returns:
            List of Recommendation objects sorted by final score descending
        """
        recommendations = []
        for candidate in candidates:
            score_result = Scorer.calculate_score(candidate, job)
            recommendation = Recommendation(candidate, score_result)
            recommendations.append(recommendation)
        
        # Sort by final score descending
        recommendations.sort(key=lambda x: x.score_result.final_score, reverse=True)
        
        return recommendations
