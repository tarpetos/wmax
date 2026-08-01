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
    Возвращает главную страницу веб-интерфейса.

    Returns:
        FileResponse: Статический HTML-файл.
    """
    logger.info("Запрошена главная страница")
    return FileResponse(str(static_dir / "index.html"))


def main() -> None:
    """
    Запускает веб-сервер Uvicorn для приложения.
    """
    logger.info("Сервер запускается на http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
