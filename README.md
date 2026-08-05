# WMAX - Maximum Weight Calculator

WMAX is a highly specialized, lightweight desktop and mobile application for calculating your One Repetition Maximum (1RM). Built with Tauri, Rust, and modern web technologies, it features an animated glassmorphism design and provides offline, lightning-fast calculations.

---

## Features
- **Accurate 1RM calculation**: Advanced algorithm utilizing specific power to endurance ratios (Power, Average, Endurance).
- **Cross-Platform Support**: Available for Windows, macOS, Linux, and Android.
- **Modern UI/UX**: Premium aesthetic with CSS-accelerated background animations, glassmorphism, and responsive design.
- **Multilingual Support**: Supports 20 languages with dynamic switching using locally bundled SVG flags for identical cross-platform rendering (fixes Windows emoji issues).
- **No Internet Required**: Fully offline and self-contained.

---

## Screenshots

<div align="center">
  <img src="assets/ui_main.png" alt="Main Interface" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);" />
  <br /><br />
  <strong>Main interface:</strong> <em>This shows the overall look of the application right after opening. It features a modern, dark glassmorphism design with an interactive language selector and background animations.</em>
</div>
<br />
<br />

<div align="center">
  <img src="assets/ui_result.png" alt="Results View" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);" />
  <br /><br />
  <strong>Calculation & results:</strong> <em>This shows the input form alongside the dynamically calculated 1RM result. Results update in real-time as you type, with an animated counter and both metric (kg) and imperial (lbs) units.</em>
</div>
<br />
<br />

<div align="center">
  <img src="assets/ui_table.png" alt="Reference Table" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);" />
  <br /><br />
  <strong>Reference table:</strong> <em>This screenshot displays the help table popup that explains the mathematics behind the power to endurance ratios. It automatically highlights the column and row based on your current inputs.</em>
</div>

---

## Getting started

### Development

The project is built using Tauri, HTML, CSS, and vanilla JavaScript.

1. **Install Dependencies**:
   Make sure you have Node.js and Rust installed on your system.
   ```bash
   npm install
   ```

2. **Run in Development Mode**:
   ```bash
   npm run tauri dev
   ```

3. **Build the Application**:
   ```bash
   npm run tauri build
   ```
   For Android:
   ```bash
   npm run tauri android build
   ```

### Releases

Pre-compiled binaries for Windows, macOS (DMG), Linux (AppImage), and Android (APK) are automatically generated via GitHub Actions. Head over to the [Releases](../../releases) page and download the package for your platform.

*Note for Linux users: If you are using a bleeding-edge distribution like Arch Linux and experience EGL/Wayland crashes with the AppImage, download the raw binary (`wmax-linux-amd64`) instead. Note that the raw binary requires `webkit2gtk-4.1` to be installed on your system (e.g., `sudo pacman -S webkit2gtk-4.1`).*

### Command-Line Arguments

The desktop executable supports several launch flags, primarily allowing you to run the app in a headless local server mode instead of a standard window:

- `--server`: Launches WMAX as a headless HTTP server serving the UI.
- `--host <IP>`: Sets the host IP for the server (defaults to `127.0.0.1`). Implicitly enables server mode.
- `--port <PORT>`: Sets the port for the server (defaults to `8080`). Implicitly enables server mode.

*Note: On Linux, WMAX automatically sets `WEBKIT_DISABLE_DMABUF_RENDERER=1` and `WEBKIT_DISABLE_COMPOSITING_MODE=1` internally to prevent known EGL WebKit crashes on certain distros (like Arch Linux), unless you have explicitly defined these environment variables yourself.*

---

## Mathematical model

The formula used dynamically estimates max capacity using a scale dependent on what type of lifter you are. The muscle profile defines the specific thresholds for reps that correspond to a given percentage of your 1RM.

### 1. Identify the Rep Thresholds Array
Depending on the chosen "Power to Endurance Ratio", a specific array of rep limits is used:

- **Power** (Fast-twitch dominant): `[1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30]`
- **Average** (Balanced fibers): `[1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38]`
- **Endurance** (Slow-twitch dominant): `[1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50]`

Each index in this array maps to a specific **% of 1RM**, starting at 100% (index 0) and dropping by 5% increments down to 50% (index 10).

### 2. Find the Percentage Multiplier ($P$)
When you enter your reps ($R$), the algorithm searches the array to find the first tier threshold that is *strictly greater* than your entered reps.
Once found at index $i$, the percentage $P$ is calculated as:
$$ P = 100 - (i - 1) \times 5 $$

*Example: If you selected the "Power" profile and entered 5 reps, the algorithm looks at the Power array. The first number strictly greater than 5 is 6 (at index 4). Therefore, $P = 100 - (4 - 1) \times 5 = 85$. This means 5 reps for a Power athlete roughly corresponds to 85% of their 1RM.*

### 3. Calculate 1RM
With $P$ determined, the baseline maximum is calculated as:
$$ \text{1RM} = \frac{\text{Weight Lifted}}{(P / 100)} $$

For weights over 50kg (or 110lbs), the final result is seamlessly rounded to the nearest standard 2.5kg interval.
