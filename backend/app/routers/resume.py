from fastapi import APIRouter,Depends,File,UploadFile,HTTPException,status
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.schemas.resume_analysis import ResumeAnalysisResponse
from app.repositories.resume_repository import ResumeRepository
from app.services.resume_service import ResumeService

router=APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)

@router.post("/upload",response_model=ResumeResponse)
def upload_resume(file:UploadFile=File(...),current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return ResumeService.upload_resume(db=db,file=file,current_user=current_user)

@router.get("/analysis",response_model=ResumeAnalysisResponse)
def get_resume_analysis(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    resume=ResumeRepository.get_by_user_id(db,current_user.id)
    if resume is None or resume.analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resume not found")
    return ResumeAnalysisResponse.model_validate(resume.analysis)

@router.get("",response_model=ResumeResponse)
def get_resume(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return ResumeService.get_resume(db=db,current_user=current_user)

@router.delete("",status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    ResumeService.delete_resume(db=db,current_user=current_user)