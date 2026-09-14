from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
import app.models  # noqa: F401 — registers every model before create_all runs

from app.api import search, ask, timetable, faculty

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(ask.router)
app.include_router(timetable.router)
app.include_router(faculty.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Campus AI Backend"}