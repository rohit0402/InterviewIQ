from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile,HTTPException,status
from app.utils.file_storage import FileStorage
from app.schemas.resume import ResumeResponse
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.core.enum import ResumeStatus
from app.models.resume import Resume
from app.services.resume_analysis_service import ResumeAnalysisService
class ResumeService:

    @staticmethod
    def upload_resume(db:Session,file:UploadFile,current_user:User)->ResumeResponse:
        if file.content_type!="application/pdf":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="only pdf files are allowed")
        
        stored_filename,file_path=FileStorage.save_resume(file)

        existing_resume=ResumeRepository.get_by_user_id(db,current_user.id)
        file_size=Path(file_path).stat().st_size

        if existing_resume:
            FileStorage.delete_resume(existing_resume.file_path)

            existing_resume.original_filename=file.filename
            existing_resume.stored_filename=stored_filename
            existing_resume.file_path=file_path
            existing_resume.file_size=file_size
            existing_resume.mime_type=file.content_type
            existing_resume.status=ResumeStatus.UPLOADED.value

            existing_resume=ResumeRepository.update(db,existing_resume)
           

            ResumeAnalysisService.analyze_resume(
                db,
                existing_resume,
            )

            return ResumeResponse.model_validate(existing_resume)
        
        resume=Resume(
            user_id=current_user.id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            status=ResumeStatus.UPLOADED.value
        )
        resume=ResumeRepository.create(db,resume)
        ResumeAnalysisService.analyze_resume(db,resume,)
        return ResumeResponse.model_validate(resume)