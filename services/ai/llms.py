from langchain_google_genai import ChatGoogleGenerativeAI

from configs import settings
from dotenv import load_dotenv
load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    temperature=settings.TEMPERATURE,
    max_retries=2,
)