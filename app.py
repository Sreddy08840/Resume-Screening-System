
import os
from config import logger, Config
from parser.resume_parser import ResumeParser
from utils.extractor import CandidateExtractor
from models.candidate import Candidate
from models.job import Job
from reports.json_handler import JSONHandler
from reports.report_generator import ReportGenerator
from matcher.recommendation import Recommender


def main():
    print("=" * 80)
    print("RESUME SCREENING SYSTEM")
    print("=" * 80)
    
    job = None
    candidates = []
    recommendations = []
    
    try:
        # Step 1: Load job requirements
        print("\nStep 1: Loading job requirements...")
        job_path = os.path.join(Config.JOBS_DIR, 'python_developer.json')
        job = JSONHandler.load_job(job_path)
        print(job.pretty_print())
        logger.info(f"Successfully loaded job: {job.title}")
    except FileNotFoundError as e:
        logger.error(f"Job file not found: {e}")
        print(f"Error: {e}")
        print("Please ensure the job file exists in data/jobs/")
        return
    except Exception as e:
        logger.error(f"Unexpected error loading job: {e}", exc_info=True)
        print(f"Unexpected error loading job: {e}")
        return
    
    try:
        # Step 2: Load and parse resumes
        print("\nStep 2: Parsing resumes...")
        resume_results = ResumeParser.parse_multiple(Config.RESUMES_DIR)
        
        if not resume_results:
            print("No resume files found in data/resumes/")
            logger.warning("No resume files found")
            return
        
        successful = sum(1 for r in resume_results if r["success"])
        failed = len(resume_results) - successful
        print(f"Processed {len(resume_results)} files: {successful} successful, {failed} failed")
        
        if failed > 0:
            print("\nFailed files:")
            for r in resume_results:
                if not r["success"]:
                    print(f"  - {r['file']}: {r['error']}")
        
        # Extract candidate information
        candidates = []
        for result in resume_results:
            if result["success"]:
                try:
                    extracted = CandidateExtractor.extract_all(result["raw_text"])
                    candidate = Candidate(
                        name=extracted["name"],
                        email=extracted["email"],
                        phone=extracted["phone"],
                        skills=extracted["skills"],
                        experience=extracted["experience"],
                        education=extracted["education"],
                        raw_text=result["raw_text"]
                    )
                    candidates.append(candidate)
                    
                    # Save parsed candidate
                    try:
                        JSONHandler.save_parsed_candidate(candidate)
                        logger.debug(f"Saved parsed candidate: {candidate.name or result['file']}")
                    except Exception as e:
                        logger.warning(f"Failed to save parsed candidate: {e}")
                
                except Exception as e:
                    logger.error(f"Failed to process candidate from {result['file']}: {e}", exc_info=True)
                    print(f"Warning: Failed to process {result['file']}")
        
        if not candidates:
            print("\nNo candidates successfully processed")
            logger.warning("No candidates successfully processed")
            return
    
    except Exception as e:
        logger.error(f"Unexpected error parsing resumes: {e}", exc_info=True)
        print(f"Error parsing resumes: {e}")
        return
    
    try:
        # Step 3: Calculate recommendations
        print("\nStep 3: Calculating recommendations...")
        recommendations = Recommender.recommend(candidates, job)
        
        if not recommendations:
            print("\nNo recommendations generated")
            logger.info("No recommendations generated")
            return
        
        print(f"\nFound {len(recommendations)} candidate(s):")
        print("=" * 80)
        for i, rec in enumerate(recommendations, 1):
            print(f"\nCandidate #{i}: {rec.recommendation}")
            print("-" * 80)
            print(rec.candidate.pretty_print())
            print(f"\nScore Breakdown:")
            print(f"  Skill Score: {rec.score_result.skill_score}")
            print(f"  Experience Score: {rec.score_result.experience_score}")
            print(f"  Final Score: {rec.score_result.final_score}")
            print("=" * 80)
    
    except Exception as e:
        logger.error(f"Unexpected error calculating recommendations: {e}", exc_info=True)
        print(f"Error calculating recommendations: {e}")
        return
    
    try:
        # Step 4: Generate reports
        if recommendations:
            print("\nStep 4: Generating reports...")
            base_filename = f"screening_{job.title.replace(' ', '_').lower()}"
            report_paths = ReportGenerator.generate_reports(job, recommendations, base_filename)
            
            print(f"Text report saved to: {report_paths['text_report']}")
            print(f"JSON report saved to: {report_paths['json_report']}")
            
            # Print text report preview
            print("\nText Report Preview:")
            print("=" * 80)
            try:
                with open(report_paths["text_report"], "r", encoding="utf-8") as f:
                    print(f.read())
            except Exception as e:
                logger.warning(f"Failed to read report preview: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error generating reports: {e}", exc_info=True)
        print(f"Error generating reports: {e}")
        return
    
    print("\n" + "=" * 80)
    print("PROCESS COMPLETED SUCCESSFULLY!")
    print(f"Log file: {os.path.join(Config.LOGS_DIR, 'resume_screening.log')}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcess interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        print("Check log file for details")
