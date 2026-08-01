import sys
from pathlib import Path
from unittest.mock import patch


def test_app_pyinstaller_path() -> None:
    with patch.object(sys, "frozen", True, create=True), patch.object(
        sys, "_MEIPASS", "/tmp/mocked", create=True
    ):
        import importlib

        import wmax.app

        importlib.reload(wmax.app)
        assert wmax.app.base_dir == Path("/tmp/mocked")

    import importlib
    import wmax.app

    importlib.reload(wmax.app)


def test_main_run() -> None:
    with (
        patch("main.uvicorn.Server.run") as mock_server_run,
        patch("main.pystray.Icon.run") as mock_icon_run,
        patch("sys.argv", ["main"])
    ):
        import main

        main.main()
        mock_server_run.assert_called_once()
        mock_icon_run.assert_called_once()
