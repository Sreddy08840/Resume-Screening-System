
import os
import logging


def setup_logging():
    """Configure logging for the application"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'resume_screening.log')
    
    # Create logger
    logger = logging.getLogger('resume_screening')
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize logger
logger = setup_logging()


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RESUMES_DIR = os.path.join(DATA_DIR, 'resumes')
    JOBS_DIR = os.path.join(DATA_DIR, 'jobs')
    PARSED_DIR = os.path.join(DATA_DIR, 'parsed')
    REPORTS_DIR = os.path.join(DATA_DIR, 'reports')
    LOGS_DIR = os.path.join(DATA_DIR, 'logs')
    
    # Weights for final score calculation
    SKILL_WEIGHT = 0.7
    EXPERIENCE_WEIGHT = 0.3
    
    MIN_SCORE_THRESHOLD = 50

