# Fingers-Counter ✋

A small computer vision project that counts how many fingers you're holding up, live from your webcam. It works with your left hand, your right hand, or both at the same time, and shows the count for each hand plus the total (up to 10).

I built it while learning OpenCV and MediaPipe, mainly to understand how hand landmark detection actually works under the hood.

<!-- Add a demo GIF here, e.g. ![demo](demo.gif) -->

## How it works

1. OpenCV grabs frames from your webcam and mirrors them, so it feels like looking in a mirror.
2. MediaPipe Hands finds up to two hands and gives 21 landmark points per hand (fingertips, knuckles, wrist), plus a label saying whether it's the left or right hand.
3. For the four fingers, a finger counts as "up" if its tip is above its middle joint.
4. The thumb moves sideways instead of up and down, so it's checked on the x-axis instead. The direction flips depending on which hand it is.

## Project structure

```
Fingers-Counter/
├── Finger_counter_.py          # main script, run this
├── HAND_TRACKING/
│   ├── __init__.py
│   └── HandTrackingModule.py   # wrapper around MediaPipe Hands
├── pyproject.toml              # dependencies (for uv)
├── uv.lock                     # exact pinned versions (for uv)
├── .python-version             # Python version uv should use
└── requirements.txt            # same dependencies, for pip users
```

## Setup

There are two ways to run this. **uv is recommended**: it installs the right Python version for you and uses the exact same package versions I tested with. If you'd rather stick with pip, that works too.

First, clone the repo (either way):

```bash
git clone https://github.com/ayushcpp/Fingers-Counter.git
cd Fingers-Counter
```

---

### Option 1: Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager. You don't need Python installed beforehand; uv downloads the correct version (3.9) by itself.

#### 1. Install uv

**Linux / macOS**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Arch Linux you can also get it from the official repos: `sudo pacman -S uv`

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, close and reopen your terminal so the `uv` command is available. Check it with:

```bash
uv --version
```

#### 2. Create the virtual environment

```bash
uv sync
```

This creates a `.venv` folder, installs Python 3.9 if needed, and installs every package at the exact version listed in `uv.lock`.

#### 3. Activate the virtual environment

**Linux / macOS (bash or zsh)**

```bash
source .venv/bin/activate
```

**Linux (fish shell)**

```fish
source .venv/bin/activate.fish
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\activate
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate.bat
```

You'll see `(fingers-counter)` at the start of your prompt once it's active.

#### 4. Run it

```bash
python Finger_counter_.py
```

> **Shortcut:** with uv you can skip steps 2 and 3 entirely and just run `uv run Finger_counter_.py`. It sets up and uses the environment automatically.

---

### Option 2: Using pip

#### 1. Make sure you have the right Python

This project uses `mediapipe==0.10.5`, which only supports **Python 3.9, 3.10, or 3.11**. Python 3.12 and newer will **not** work, because pip won't find a matching mediapipe build.

Check your version:

```bash
python --version
```

If you're on 3.12+, install Python 3.11 from [python.org](https://www.python.org/downloads/) (Windows/macOS) or your distro's package manager (Linux).

#### 2. Create and activate a virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If you have several Python versions on Windows, you can pick one explicitly with the launcher, e.g. `py -3.11 -m venv .venv`.

#### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run it

```bash
python Finger_counter_.py
```

---

## Usage

- Hold your hand(s) up in front of the webcam, **palm facing the camera**.
- The count for each hand appears on the left side of the window, with the total at the top.
- Press **Esc** to quit.

## Troubleshooting

**PowerShell says running scripts is disabled when activating the venv**
Run this once, then try activating again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**The camera doesn't open (Windows)**
Go to *Settings → Privacy & security → Camera* and make sure "Let desktop apps access your camera" is on. Also close any other app using the camera (Teams, Zoom, etc.); Windows only lets one app use it at a time.

**Wrong camera or a weird grey image**
Some laptops have an extra IR camera (used for Windows Hello). Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `Finger_counter_.py`.

**The image is very dark (Linux)**
Your webcam might be stuck in manual exposure mode. Install `v4l-utils` and switch it back to auto:

```bash
v4l2-ctl -d /dev/video0 -c auto_exposure=3
```

**`qt.qpa.plugin: Could not find the Qt platform plugin "wayland"` (Linux)**
This is just a warning, and the window still opens through XWayland. To hide it, run with `QT_QPA_PLATFORM=xcb python Finger_counter_.py`.

**Thumb count is wrong**
The thumb check assumes your palm is facing the camera. If you show the back of your hand, the thumb result flips. Good lighting in front of you (not behind) also helps a lot.

## Built with

- [OpenCV](https://opencv.org/): webcam capture and drawing
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker): hand landmark detection
- [uv](https://docs.astral.sh/uv/): dependency and environment management

## License

MIT, see [LICENSE](LICENSE).