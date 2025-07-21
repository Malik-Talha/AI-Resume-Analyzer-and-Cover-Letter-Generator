from langchain_core.output_parsers import StrOutputParser

from data_models.models import ResumeData
from .prompts import EXTRACT_RESUME_DATA, WRITE_COVER_LETTER
from .llms import gemini as __gemini


def get_resume_extraction_chain():
    """ get a chain to extract structured data from an unstructured resume text """

    chain = EXTRACT_RESUME_DATA | __gemini.with_structured_output(ResumeData)

    return chain 

def get_cover_writer_chain():
    """ get a chain that writes cover letter for you for applying on a job """

    chain = WRITE_COVER_LETTER | __gemini | StrOutputParser()

    return chain