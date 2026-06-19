
class JobLoaderError(Exception):
    """Base exception for job loader errors"""
    pass


class InvalidJSONError(JobLoaderError):
    """Raised when JSON is invalid"""
    pass


class MissingRequiredFieldError(JobLoaderError):
    """Raised when a required field is missing"""
    pass


class InvalidJobDataError(JobLoaderError):
    """Raised when job data is invalid"""
    pass

