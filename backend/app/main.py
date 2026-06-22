from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .api import text, report, history, upload

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI 英文语篇深度研读系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

export_dir = Path(__file__).resolve().parent.parent / "exports"
export_dir.mkdir(exist_ok=True)
app.mount("/exports", StaticFiles(directory=str(export_dir)), name="exports")

app.include_router(text.router, prefix="/api/v1/english")
app.include_router(report.router, prefix="/api/v1/english")
app.include_router(history.router, prefix="/api/v1/english")
app.include_router(upload.router, prefix="/api/v1/english")

@app.get("/api/v1/english/health")
async def health():
    return {"status": "ok", "service": "english-discourse-reading"}
