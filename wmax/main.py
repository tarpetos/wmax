import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from wmax.api import router

app = FastAPI(title="Weight Max Calculator")

app.include_router(router)

# Handle PyInstaller path for static files
if getattr(sys, "frozen", False):
    # If bundled via PyInstaller, use _MEIPASS
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(base_dir, "static")

# Make sure static directory exists (mostly for development)
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(os.path.join(static_dir, "index.html"))


def main() -> None:
    print("Starting server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
