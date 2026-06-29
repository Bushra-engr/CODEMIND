from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.routes.register import router as register_router
from backend.routes.login import router as login_router
from backend.routes.coderuns import router as analyze_router
from backend.routes.history import router as history_router
from backend.routes.github import router as github_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(
    title="AI Powered Coding Assistant",
    description="Backend Server with Neon Postgres and JWT",
    version = "1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend" / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "frontend" / "templates"/"index.html"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

    
app.include_router(register_router)

app.include_router(login_router)

app.include_router(analyze_router)

app.include_router(history_router)

app.include_router(github_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
     
@app.get("/health")
def health_check():
    return {
        "health_status":"ok"
    }

