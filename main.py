from fastapi import FastAPI, UploadFile, File
import uvicorn

from typing import Annotated


from services.pdf_service import extract_pdf

#********************************************************
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#***************************************************

app = FastAPI(
    title="AI Resume Analyzer and Cover letter Writer",
)


@app.get("/")
def root():

    return {"message": "welcome to the root"}


@app.post("/upload_file")
async def analyze_resume(resume: UploadFile):
    
    # # reading file as bytes
    # resume_bytes = await resume.read()
    
    # extracting the data
    return {"text": await extract_pdf(resume)}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )