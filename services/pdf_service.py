import pdfplumber
from pathlib import Path

from io import BytesIO

from fastapi import UploadFile

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


resume = Path().resolve() / "services/Resume 2025.pdf"
# logger.debug(resume)

def extract_pdf(path: Path)->list[dict]:
    """ Extract text from the PDF Pages """

    logger.info(f"Reading PDf file: {path.name}")
    pages_data=[]
    with pdfplumber.open(resume) as pdf:
        metadata = pdf.metadata
        for i, page in enumerate(pdf.pages):
            metadata["page_no"] = i+1  
            pages_data.append({"text": page.extract_text(), "metadata": metadata})

    logger.info(f"Text extracted from {resume.name} Successfully!")

    return pages_data


async def extract_pdf(pdf_file: UploadFile)->list[dict]:
    """ Extract text from the PDF Pages provided as bytes """

    logger.info(f"Reading PDf file: {pdf_file.filename}")
    # pdf_bytes = await pdf.read()

    pages_data=[]
    with pdfplumber.open(BytesIO(await pdf_file.read())) as pdf:
        metadata = pdf.metadata
        for i, page in enumerate(pdf.pages):
            metadata["page_no"] = i+1  
            pages_data.append({"text": page.extract_text(), "metadata": metadata})

    logger.info(f"Text extracted from {pdf_file.filename} Successfully!")

    return pages_data
