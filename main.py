import os

from fastapi import FastAPI, UploadFile, File
import uvicorn

from langchain_core.runnables import Runnable

from data_models.models import ResumeData, JobDescription, Tone
from services.pdf_service import extract_pdf
from services.ai.ai_service import get_resume_extraction_chain, get_cover_writer_chain

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


@app.post("/write_cover_letter")
# async def analyze_resume(job_description: JobDescription, tone: Tone, resume: UploadFile):
async def analyze_resume(job_title: str, job_description: str, tone: Tone, resume: UploadFile):
    
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



if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )