import re
import os
from typing import Dict, Any
import docx
from PyPDF2 import PdfReader

class JDParser:
    """
    Parser for UN Job Descriptions.
    Supports .docx and .pdf formats.
    """
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        
        if ext == ".docx":
            text = JDParser._extract_text_from_docx(file_path)
        elif ext == ".pdf":
            text = JDParser._extract_text_from_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return JDParser._extract_info(text)

    @staticmethod
    def _extract_text_from_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def _extract_text_from_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    @staticmethod
    def _extract_info(text: str) -> Dict[str, Any]:
        """
        Regex-based extraction of key fields.
        Adjust patterns based on representative UN JD samples.
        """
        # Clean text: remove multiple newlines and normalize spaces
        text_lines = [line.strip() for line in text.split('\n') if line.strip()]
        first_line = text_lines[0] if text_lines else "Unknown"

        info = {
            "job_title": first_line,  # Fallback to first line
            "deadline": "N/A",
            "department": "N/A",
            "duty_station": "N/A",
            "id": "N/A"
        }
        
        # Patterns updated based on UN Inspira / ESCAP sample
        patterns = {
            "job_title": [
                r"Title\s*:\s*(.*)", 
                r"Position Title\s*:\s*(.*)", 
                r"Job Title\s*:\s*(.*)"
            ],
            "deadline": [
                r"Deadline\s*:\s*([A-Za-z]+\s\d{1,2},\s\d{4})", # Jan 2, 2026
                r"Deadline\s*:\s*(\d{1,2}\s[A-Za-z]+\s\d{4})", # 2 Jan 2026
                r"Posting Period\s*:\s*.*-\s*(\d{1,2}\s\w+\s\d{4})"
            ],
            "department": [
                r"Department\s*/\s*Office\s*:\s*(.*)", 
                r"Department/Office\s*:\s*(.*)", 
                r"Organe\s*:\s*(.*)"
            ],
            "duty_station": [r"Duty Station\s*:\s*(.*)", r"Lieu d'affectation\s*:\s*(.*)"],
            "id": [r"Job Opening ID\s*:\s*(\d+)", r"Numéro de l'ouverture de poste\s*:\s*(\d+)"]
        }
        
        for key, p_list in patterns.items():
            for p in p_list:
                match = re.search(p, text, re.IGNORECASE)
                if match:
                    val = match.group(1).strip()
                    # For job_title, only update if matched explicitly; otherwise keep first_line
                    if key != "job_title" or (key == "job_title" and val):
                        info[key] = val
                    break
        
        return info
