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
from PIL import Image

from wmax.app import app, static_dir

try:
    import pystray

    HAS_PYSTRAY = True
except Exception:
    HAS_PYSTRAY = False


def can_use_tray(server_mode: bool) -> bool:
    if server_mode or not HAS_PYSTRAY:
        return False
    if sys.platform.startswith("linux"):
        if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            return False
    return True


def main() -> None:
    """
    Starts the Uvicorn web server for the application.
    """
    parser = argparse.ArgumentParser(description="WMAX - One Rep Max Calculator")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP to bind the server to")
    parser.add_argument("--port", type=int, default=8372, help="Port to bind the server to")
    parser.add_argument(
        "--server-mode", action="store_true", help="Run in server mode (hides exit button and disables tray)"
    )
    args = parser.parse_args()

    if args.server_mode:
        os.environ["WMAX_SERVER_MODE"] = "1"

    logger.info("Server starting on http://{}:{}", args.host, args.port)

    def open_browser() -> None:
        time.sleep(1.5)
        webbrowser.open(f"http://{args.host}:{args.port}")

    def exit_app(icon, _item) -> None:  # noqa: ANN001
        if icon:
            icon.stop()
        os._exit(0)

    if can_use_tray(args.server_mode):
        server = uvicorn.Server(uvicorn.Config(app, host=args.host, port=args.port, log_config=None))
        threading.Thread(target=server.run, daemon=True).start()
        threading.Thread(target=open_browser, daemon=True).start()

        icon_path = static_dir / "favicon.ico"
        try:
            image = Image.open(icon_path)
        except Exception:
            image = Image.new("RGB", (64, 64), color="black")

        menu = pystray.Menu(
            pystray.MenuItem(
                "Open in Browser", lambda: webbrowser.open(f"http://{args.host}:{args.port}"), default=True
            ),
            pystray.MenuItem("Exit", exit_app),
        )
        icon = pystray.Icon("wmax", image, "WMAX Server", menu)
        icon.run()
    else:
        threading.Thread(target=open_browser, daemon=True).start()
        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Prevent Uvicorn and asyncio from printing messy tracebacks on Ctrl+C
        print("\nServer stopped.")
        os._exit(0)
