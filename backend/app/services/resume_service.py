from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile,HTTPException,status
from app.utils.file_storage import FileStorage
from app.schemas.resume import ResumeResponse
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.core.enum import ResumeStatus
from app.models.resume import Resume
from app.repositories.resume_analysis_repository import (
    ResumeAnalysisRepository,
)
from app.tasks.resume_tasks import process_resume_task

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
    def upload_resume(
        db: Session,
        file: UploadFile,
        current_user: User,
    ) -> ResumeResponse:

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed",
            )

        file_path = None

        try:
            stored_filename, file_path = FileStorage.save_resume(file)

            existing_resume = ResumeRepository.get_by_user_id(
                db,
                current_user.id,
            )

            file_size = Path(file_path).stat().st_size

            if existing_resume:

                FileStorage.delete_resume(existing_resume.file_path)

                existing_resume.original_filename = file.filename
                existing_resume.stored_filename = stored_filename
                existing_resume.file_path = file_path
                existing_resume.file_size = file_size
                existing_resume.mime_type = file.content_type

                ResumeRepository.update_status(
                    db=db,
                    resume=existing_resume,
                    status=ResumeStatus.PENDING,
                )

                try:
                    process_resume_task.delay(existing_resume.id)
                except Exception:
                    ResumeRepository.update_status(
                        db=db,
                        resume=existing_resume,
                        status=ResumeStatus.FAILED,
                    )

                    FileStorage.delete_resume(file_path)

                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to queue resume processing",
                    )

                return ResumeService._to_resume_response(existing_resume)

            resume = Resume(
                user_id=current_user.id,
                original_filename=file.filename,
                stored_filename=stored_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type,
                status=ResumeStatus.PENDING,
            )

            resume = ResumeRepository.create(db, resume)

            try:
                process_resume_task.delay(resume.id)

            except Exception:

                ResumeRepository.update_status(
                    db=db,
                    resume=resume,
                    status=ResumeStatus.FAILED,
                )

                FileStorage.delete_resume(file_path)

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to queue resume processing",
                )

            return ResumeService._to_resume_response(resume)

        except HTTPException:
            raise

        except Exception:

            if file_path:
                FileStorage.delete_resume(file_path)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload resume",
            )

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
