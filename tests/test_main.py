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
    with patch("main.uvicorn.run") as mock_run, patch("sys.argv", ["main"]):
        import main

        main.main()
        import wmax.app
        mock_run.assert_called_once_with(wmax.app.app, host="127.0.0.1", port=8372)
