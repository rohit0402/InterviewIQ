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