import uuid

from fastapi import UploadFile

from app.core.supabase import supabase


BUCKET_NAME = "resumes"


class FileStorage:

    @staticmethod
    def save_resume(file: UploadFile):

        extension = file.filename.split(".")[-1]

        stored_filename = f"{uuid.uuid4()}.{extension}"

        file_bytes = file.file.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            path=stored_filename,
            file=file_bytes,
            file_options={
                "content-type": file.content_type,
            },
        )

        return stored_filename, stored_filename

    @staticmethod
    def delete_resume(file_path: str):

        supabase.storage.from_(BUCKET_NAME).remove(
            [file_path]
        )

    @staticmethod
    def get_public_url(file_path: str):

        return (
            supabase.storage
            .from_(BUCKET_NAME)
            .get_public_url(file_path)
        )