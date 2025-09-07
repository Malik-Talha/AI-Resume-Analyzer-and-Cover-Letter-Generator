import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):

    return templates.TemplateResponse("index.html", context={"request": request})


app.include_router(cover_letter.router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )