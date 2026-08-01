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

import pystray
import uvicorn
from loguru import logger
from PIL import Image

from wmax.app import app, static_dir


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

    def exit_app(icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        icon.stop()
        os._exit(0)

    # Run Uvicorn in a background thread
    server = uvicorn.Server(uvicorn.Config(app, host=args.host, port=args.port, log_config=None))
    threading.Thread(target=server.run, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()

    # Setup System Tray in the main thread
    icon_path = static_dir / "favicon.ico"
    try:
        image = Image.open(icon_path)
    except Exception:
        image = Image.new("RGB", (64, 64), color="black")

    menu = pystray.Menu(
        pystray.MenuItem("Open in Browser", lambda: webbrowser.open(f"http://{args.host}:{args.port}")),
        pystray.MenuItem("Exit", exit_app),
    )
    icon = pystray.Icon("wmax", image, "WMAX Server", menu)
    icon.run()


if __name__ == "__main__":
    main()
