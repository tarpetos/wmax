import argparse
import os
import sys
import threading
import time
import webbrowser

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")  # noqa: SIM115
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")  # noqa: SIM115

import uvicorn
from loguru import logger

from wmax.app import app


def main() -> None:
    """
    Starts the Uvicorn web server for the application.
    """
    parser = argparse.ArgumentParser(description="WMAX - One Rep Max Calculator")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP to bind the server to")
    parser.add_argument("--port", type=int, default=8372, help="Port to bind the server to")
    args = parser.parse_args()

    logger.info("Server starting on http://{}:{}", args.host, args.port)

    def open_browser() -> None:
        time.sleep(1.5)
        webbrowser.open(f"http://{args.host}:{args.port}")

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
