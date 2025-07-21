import os

from fastapi import FastAPI

from routers import cover_letter

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

    return {"message": "welcome home!"}


app.include_router(cover_letter.router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )