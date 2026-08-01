import argparse
import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from wmax.api import router

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

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


def main() -> None:
    """
    Starts the Uvicorn web server for the application.
    """
    parser = argparse.ArgumentParser(description="WMAX - One Rep Max Calculator")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP to bind the server to")
    parser.add_argument("--port", type=int, default=8372, help="Port to bind the server to")
    args = parser.parse_args()

    logger.info("Server starting on http://%s:%d", args.host, args.port)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
