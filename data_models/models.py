from pydantic import BaseModel, Field
from enum import Enum

class ResumeData(BaseModel):
    """Required Data from a Resume """

    name: str = Field(description="Name of the candidate")
    experience: str = Field(description="Experience of the candidate e.g. years, domain etc. Extract COMPLETE experience.")
    skills: list[str] = Field(description="Skills mentioned in the resume of the candidate")
    projects: list[str] = Field(description="projects that the candidate has worked on, if present.")

# {

#   "name": "Ayesha Khan",

#   "experience": "3 years in data science, working with NLP and time-series forecasting.",

#   "skills": ["Python", "TensorFlow", "Pandas", "Prompt Engineering"],

#   "projects": ["AI-powered chatbot for finance", "Anomaly detection for manufacturing sensors"]

# }

class JobDescription(BaseModel):
    """ Job Description the candidate is applying on """
    job_title: str = Field(description="title of the job/position")
    job_requirements: list[str] = Field(description="Any requirements to get the job e.g. skills, experience")

class Tone(str, Enum):
    confident = "Confident"
    professional = "Professional"
    creative = "Creative"
    enthusiastic = "Enthusiastic"
    humble = "Humble"
    direct = "Direct"