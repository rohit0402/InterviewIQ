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
from app.repositories.resume_analysis_repository import (
    ResumeAnalysisRepository,
)


class ResumeService:
    @staticmethod
    def _to_resume_response(resume: Resume) -> ResumeResponse:
        return ResumeResponse(
            id=resume.id,
            original_filename=resume.original_filename,
            file_size=resume.file_size,
            mime_type=resume.mime_type,
            status=resume.status,
            analysis_available=resume.analysis is not None,
            created_at=resume.created_at,
        )


    @staticmethod
    def upload_resume(db: Session,file: UploadFile,current_user: User,) -> ResumeResponse:

        if file.content_type != "application/pdf":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only PDF files are allowed",)

        stored_filename, file_path = FileStorage.save_resume(file)

        try:
            existing_resume = ResumeRepository.get_by_user_id(db,current_user.id,)

            file_size = Path(file_path).stat().st_size

            if existing_resume:

                # Delete old PDF
                FileStorage.delete_resume(existing_resume.file_path)

                existing_resume.original_filename = file.filename
                existing_resume.stored_filename = stored_filename
                existing_resume.file_path = file_path
                existing_resume.file_size = file_size
                existing_resume.mime_type = file.content_type
                existing_resume.status = ResumeStatus.UPLOADED

                existing_resume = ResumeRepository.update(db,existing_resume,)

                try:
                    ResumeAnalysisService.analyze_resume(db,existing_resume,)
                except Exception:
                    existing_resume.status = ResumeStatus.FAILED
                    ResumeRepository.update(db, existing_resume)
                    raise

                return ResumeService._to_resume_response(existing_resume)

            resume = Resume(
                user_id=current_user.id,
                original_filename=file.filename,
                stored_filename=stored_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type,
                status=ResumeStatus.UPLOADED,
            )

            resume = ResumeRepository.create(db,resume, )

            try:
                ResumeAnalysisService.analyze_resume(db,resume,)
            except Exception:
                resume.status = ResumeStatus.FAILED
                ResumeRepository.update(db, resume)
                raise

            return ResumeService._to_resume_response(resume)

        except Exception:
            FileStorage.delete_resume(file_path)
            raise

    @staticmethod
    def get_resume(db: Session, current_user:User) -> ResumeResponse:
        resume = ResumeRepository.get_by_user_id(db,current_user.id,)
        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )
        return ResumeService._to_resume_response(resume)
    
    @staticmethod
    def delete_resume(db: Session,current_user:User):
        resume = ResumeRepository.get_by_user_id(db,current_user.id,)
        if resume is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resume not found",)
        FileStorage.delete_resume(resume.file_path)
        if resume.analysis :
            ResumeAnalysisRepository.delete(db,resume.analysis)

        ResumeRepository.delete(db,resume)
