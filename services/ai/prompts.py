from langchain.prompts import ChatPromptTemplate

#**********************
__extract_resume_data = """You are a helpful assistant. You extract Resume information in a structured form
from a provided unstructered text of a resume. Be careful and extract each peace of information meticulously!"""

EXTRACT_RESUME_DATA = ChatPromptTemplate.from_messages([
    ("system", __extract_resume_data),
    ("human", "following is the unstructured resume text. Please extract the required resume data.\nText:\n*****\n{resume_text}\n*****")
])
#************************************
#***********

#**********************
__write_cover_letter = """You are a helpful assistant. You write a strong yet concise cover letter that convinces the recruiter
to hire the candidate. You will be provided with the candidate resume data and the job description applying for. ONLY write the 
cover letter; not other comments please. Start from the main body (dont use any blanks!)"""

WRITE_COVER_LETTER = ChatPromptTemplate.from_messages([
    ("system", __write_cover_letter),
    ("human", "write a powerful cover letter for me to get the role for the following job. Write the cover letter that shows me {mode} (the tone of the cover letter).\n"
    "My Resume/CV:\n{resume_data}\n\nThe job I'm applying on:\n{job_desc}")
])
#************************************
#***********