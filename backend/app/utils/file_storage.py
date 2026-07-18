import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR=Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

class FileStorage:

    @staticmethod
    def save_resume(file:UploadFile):
        extension=Path(file.filename).suffix

        stored_filename=f"{uuid.uuid4()}{extension}"
        file_path=UPLOAD_DIR/stored_filename
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        return stored_filename, str(file_path)
    
    @staticmethod
    def delete_resume(file_path:str):
        path=Path(file_path)
        if path.exists():
            path.unlink()