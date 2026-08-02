import fitz

from app.core.supabase import supabase


BUCKET_NAME = "resumes"


class PdfService:

    @staticmethod
    def extract_text(file_path: str) -> str:

        try:
            response = (
                supabase.storage
                .from_(BUCKET_NAME)
                .download(file_path)
            )

            document = fitz.open(
                stream=response,
                filetype="pdf",
            )

            pages = []

            for page in document:
                pages.append(page.get_text())

            document.close()

            return "\n".join(pages).strip()

        except Exception as e:
            raise Exception(
                f"Error extracting text from PDF: {e}"
            )