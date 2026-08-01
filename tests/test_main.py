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
    with patch("sys.argv", ["main"]):
        import main
        main.HAS_PYSTRAY = False
        with patch("main.uvicorn.run") as mock_run:
            main.main()
            mock_run.assert_called_once()
