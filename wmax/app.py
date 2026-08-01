import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from wmax.api import router

app = FastAPI(title="Weight Max Calculator")
app.include_router(router)

if getattr(sys, "frozen", False):
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).resolve().parent

static_dir = base_dir / "static"
static_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def read_index() -> FileResponse:
    """
    Returns the main page of the web application.

    Returns:
        FileResponse: Static HTML file.
    """
    logger.info("Main page requested")
    return FileResponse(str(static_dir / "index.html"))
