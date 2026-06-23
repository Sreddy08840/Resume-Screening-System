
"""FastAPI backend for Resume Screening System"""
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

from config import logger, Config
from parser.resume_parser import ResumeParser
from utils.extractor import CandidateExtractor
from models.candidate import Candidate
from models.job import Job
from reports.json_handler import JSONHandler
from reports.report_generator import ReportGenerator
from matcher.recommendation import Recommender


# Initialize FastAPI app
app = FastAPI(
    title="Resume Screening System API",
    description="Professional resume screening and candidate recommendation system",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create necessary directories
for dir_path in [
    Config.RESUMES_DIR,
    Config.JOBS_DIR,
    Config.PARSED_DIR,
    Config.REPORTS_DIR,
    Config.LOGS_DIR
]:
    os.makedirs(dir_path, exist_ok=True)


@app.get("/")
async def root():
    """Root endpoint - system health check"""
    return {
        "status": "ok",
        "message": "Resume Screening System API is running!"
    }


@app.get("/api/job/{job_name}")
async def get_job(job_name: str):
    """Get job requirements by name"""
    try:
        job_path = os.path.join(Config.JOBS_DIR, f"{job_name}.json")
        job = JSONHandler.load_job(job_path)
        return {
            "status": "success",
            "job": job.to_dict()
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        logger.error(f"Error loading job: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/jobs")
async def list_jobs():
    """List all available job requirements"""
    jobs = []
    try:
        for filename in os.listdir(Config.JOBS_DIR):
            if filename.endswith(".json"):
                job_path = os.path.join(Config.JOBS_DIR, filename)
                job_name = filename.replace(".json", "")
                try:
                    job = JSONHandler.load_job(job_path)
                    jobs.append({"name": job_name, "title": job.title})
                except Exception as e:
                    logger.warning(f"Could not load {filename}: {e}")
        return {"status": "success", "jobs": jobs}
    except Exception as e:
        logger.error(f"Error listing jobs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/job")
async def create_job(job_data: Dict[str, Any]):
    """Create a new job requirement"""
    try:
        job = Job.from_dict(job_data)
        filename = job.title.replace(" ", "_").lower()
        job_path = os.path.join(Config.JOBS_DIR, f"{filename}.json")
        JSONHandler.save_job(job, job_path)
        return {"status": "success", "message": "Job created successfully"}
    except Exception as e:
        logger.error(f"Error creating job: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload multiple resume files"""
    try:
        saved_files = []
        for file in files:
            file_location = os.path.join(Config.RESUMES_DIR, file.filename)
            with open(file_location, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            saved_files.append(file.filename)
        return {
            "status": "success",
            "message": f"Successfully uploaded {len(saved_files)} files",
            "files": saved_files
        }
    except Exception as e:
        logger.error(f"Error uploading files: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/resumes")
async def list_resumes():
    """List all uploaded resumes"""
    try:
        resumes = []
        for filename in os.listdir(Config.RESUMES_DIR):
            if filename.lower().endswith(('.pdf', '.docx', '.txt')):
                resumes.append(filename)
        return {"status": "success", "resumes": resumes}
    except Exception as e:
        logger.error(f"Error listing resumes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/screen/{job_name}")
async def screen_resumes(job_name: str):
    """Screen all uploaded resumes against a job requirement"""
    try:
        # Load job
        job_path = os.path.join(Config.JOBS_DIR, f"{job_name}.json")
        job = JSONHandler.load_job(job_path)
        
        # Parse all resumes
        resume_results = ResumeParser.parse_multiple(Config.RESUMES_DIR)
        
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
                except Exception as e:
                    logger.error(f"Failed to process candidate: {e}")
        
        if not candidates:
            return {
                "status": "success",
                "message": "No valid candidates found",
                "recommendations": [],
                "failed_files": [r for r in resume_results if not r["success"]]
            }
        
        # Calculate recommendations
        recommendations = Recommender.recommend(candidates, job)
        
        # Generate reports
        base_filename = f"screening_{job_name}"
        report_paths = ReportGenerator.generate_reports(job, recommendations, base_filename)
        
        return {
            "status": "success",
            "message": "Screening complete",
            "recommendations": [rec.to_dict() for rec in recommendations],
            "reports": report_paths,
            "failed_files": [r for r in resume_results if not r["success"]]
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        logger.error(f"Error screening resumes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/reports/{report_name}")
async def download_report(report_name: str):
    """Download generated reports"""
    try:
        file_path = os.path.join(Config.REPORTS_DIR, report_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Report not found")
        return FileResponse(path=file_path, filename=report_name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
