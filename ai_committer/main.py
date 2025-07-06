from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pathlib

app = FastAPI()

# Path setup
BASE_DIR = pathlib.Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# Mount static assets (JS, CSS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Set up Jinja2 template rendering
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Root route: Flashcard dashboard or home
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
