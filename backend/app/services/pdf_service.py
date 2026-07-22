import fitz


class PdfService:

    @staticmethod
    def extract_text(file_path:str)->str:
        try:
            document=fitz.open(file_path)
            pages=[]
            for page in document:
                pages.append(page.get_text())
            document.close()
            return "\n".join(pages).strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")
        