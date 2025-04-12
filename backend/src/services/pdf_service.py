import io
import PyPDF2
from fastapi import HTTPException

class PDFService:
    @staticmethod
    def extract_text(pdf_bytes: bytes) -> str:
        """
        Extract text from a PDF file in bytes using PyPDF2.
        Returns a string with all pages/words concatenated.
        """
        try:
            all_text = ""
            with io.BytesIO(pdf_bytes) as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    all_text += page_text + "\n"
            return all_text.strip()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting text from PDF: {str(e)}"
            ) 