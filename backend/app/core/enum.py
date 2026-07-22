from enum import Enum

class UserRole(Enum):
    ADMIN="admin"
    COMPANY="company"
    CANDIDATE="candidate"

class ResumeStatus(Enum):
    UPLOADED="uploaded"
    PROCESSING="processing"
    COMPLETED="completed"
    FAILED="failed"

class InterviewStatus(Enum):
    CREATED="CREATED"
    QUESTIONS_GENERATED="QUESTIONS_GENERATED"
    IN_PROGRESS="IN_PROGRESS"
    COMPLETED="COMPLETED"
    FAILED="FAILED"