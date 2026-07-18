from fastapi import APIRouter,Depends,File,UploadFile,HTTPException,status
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService

router=APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)

@router.post("/upload",response_model=ResumeResponse)
def upload_resume(File:UploadFile=File(...),current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return ResumeService.upload_resume(db=db,file=File,current_user=current_user)