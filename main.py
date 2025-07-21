import os

from fastapi import FastAPI, UploadFile, status, HTTPException

from langchain_core.runnables import Runnable

from data_models.models import ResumeData, JobDescription, Tone
from services.pdf_service import extract_pdf
from services.ai.ai_service import get_resume_extraction_chain, get_cover_writer_chain

import uvicorn

# from dotenv import load_dotenv
# load_dotenv()

# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


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


@app.post("/cover-letter/resume")
# async def analyze_resume(job_description: JobDescription, tone: Tone, resume: UploadFile):
async def analyze_resume_and_write_cover_letter(job_title: str, job_description: str, tone: Tone, resume: UploadFile):
    """ write a cover letter by analyzing the uploaded resume (PDF Only!) and by observing the job description """

    if resume.content_type != "application/pdf": 
        logger.critical(f"The uploaded file \"{resume.filename}\" is not a PDF!")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type. Expected PDF, but got {resume.content_type}."
        )
    
    elif (resume.size/1000000) > 5: # if pdf is more than 5 MB
        logger.critical(f"The size of the uploaded file ({resume.size/1000000:.2f} MB) is exceeding the 5 MB limit!")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"The size of the PDF (resume) you uploaded is {resume.size/1000000:.2f} MB which is exceeding the 5 MB limit!"
        )

    # extract resume text
    text = await extract_pdf(resume)

    # structurize the required resume data using an LLM chain
    logger.info("Extracting required data from the Resume using the LLM Chain...")
    resume_data_extractor: Runnable = get_resume_extraction_chain()
    resume_data: ResumeData = resume_data_extractor.invoke({
        "resume_text": text
    })
    
    # write a cover letter using an LLM chain
    logger.info("Writing the cover letter using the LLM Chain...")
    cover_writer: Runnable = get_cover_writer_chain()
    cover_letter: str = cover_writer.invoke({
        "mode": tone,
        "resume_data": resume_data.model_dump(),
        # "job_desc": job_description.model_dump(),
        "job_desc": {"job_title": job_title, "job_description": job_description},
    })
    
    logger.info("Cover Letter written Successfully!")
    # return the cover letter
    return {"cover_letter": cover_letter}


@app.post("/cover-letter/form")
def write_cover_letter_from_form(profile: ResumeData, job_description: JobDescription, tone: Tone):
    """ write cover letter by analyzing experience and job description from a form """

    # write a cover letter using an LLM chain
    logger.info("Writing the cover letter using the LLM Chain...")
    cover_writer: Runnable = get_cover_writer_chain()
    cover_letter: str = cover_writer.invoke({
        "mode": tone,
        "resume_data": profile.model_dump(),
        "job_desc": job_description.model_dump(),
    })
    
    logger.info("Cover Letter written Successfully!")
    # return the cover letter
    return {"cover_letter": cover_letter}



if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )