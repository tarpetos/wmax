import sys
from pathlib import Path
from unittest.mock import patch


def test_main_pyinstaller_path() -> None:
    with patch.object(sys, "frozen", True, create=True), patch.object(
        sys, "_MEIPASS", "/tmp/mocked", create=True
    ):
        import importlib

        import wmax.main

        importlib.reload(wmax.main)
        assert wmax.main.base_dir == Path("/tmp/mocked")

    import importlib
    import wmax.main

    importlib.reload(wmax.main)


def test_main_run() -> None:
    with patch("wmax.main.uvicorn.run") as mock_run:
        import wmax.main

        wmax.main.main()
        mock_run.assert_called_once()
