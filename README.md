# WMAX - Maximum Weight Calculator

WMAX is a highly specialized web application and standalone utility for calculating your One Repetition Maximum (1RM). It's built with modern web aesthetics in mind, featuring glassmorphism and an animated design, backed by a robust, fully-tested FastAPI core.

## Features
- **Accurate 1RM Calculation**: Advanced algorithm utilizing specific muscle fiber ratios (Power, Average, Endurance).
- **FastAPI Backend**: Lightning-fast endpoints with Pydantic data validation.
- **Modern UI/UX**: Premium aesthetic with micro-animations, glassmorphism, and responsive design.
- **Standalone Executables**: Packaged via PyInstaller into single executable files for Windows, macOS, and Linux. No installation required.

## Getting Started

### Development

The project uses `uv` for lightning-fast dependency management.

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Install dependencies**:
   ```bash
   uv sync
   ```
3. **Run the server**:
   ```bash
   uv run python -m wmax.main
   ```
4. **Visit**: `http://127.0.0.1:8372`

### Running the Executable

Simply head over to the [Releases](../../releases) page and download the executable for your platform.
Double-click it (or run it from the terminal), and it will automatically spawn a local web server at `http://127.0.0.1:8372`.

## Architecture & Best Practices

- **120 Line Length limit** utilizing `Ruff`.
- **100% Test Coverage** powered by `pytest`.
- **CI/CD** automatically runs tests and builds the cross-platform releases on GitHub Actions.
- **Self-contained static files**: The app serves frontend assets efficiently from the packaged binary itself using PyInstaller's `sys._MEIPASS` runtime unpacking.

## Mathematical Model
The formula used dynamically estimates max capacity using a scale dependent on what type of lifter you are:
- **Power** (Fast-twitch dominant)
- **Average** (Balanced fibers)
- **Endurance** (Slow-twitch dominant)

Each mode scales reps to specific percentages of 1RM uniquely to provide realistic expectations based on individual genetic predispositions.