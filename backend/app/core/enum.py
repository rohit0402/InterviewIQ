from enum import Enum

class UserRole(Enum):
    ADMIN="admin"
    COMPANY="company"
    CANDIDATE="candidate"

class ResumeStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class InterviewStatus(str, Enum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    REPORT_GENERATING = "REPORT_GENERATING"
    REPORT_READY = "REPORT_READY"
    FAILED = "FAILED"