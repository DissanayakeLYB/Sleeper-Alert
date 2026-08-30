# Sleeper Alert

Monitors your webcam in real time and alerts you with a sound when you start falling asleep. Works in the background so you can focus on your work.

## Install

Requires **Python 3.8+** and a webcam.

```bash
# Clone the repo
git clone https://github.com/DissanayakeLYB/Sleeper-Alert.git
cd Sleeper-Alert

# Install dependencies
pip install -r requirements.txt
```

A small model file (`face_landmarker.task`) is downloaded automatically on first run.

## Usage

### Normal mode (with camera preview)

```bash
python drowsiness_detector.py
```

A window shows your webcam feed with eye tracking. Press **q** to quit.

### Headless mode (no camera window)

```bash
python drowsiness_detector.py --no-display
```

Runs silently in the terminal with no window — just work on your things. You'll hear a beep if drowsiness is detected. Press **Ctrl+C** to stop.

### All options

| Flag | Default | Description |
|------|---------|-------------|
| `--no-display` | off | Hide camera window. Stop with Ctrl+C |
| `--ear-threshold` | 0.20 | Eye closure sensitivity (lower = stricter) |
| `--sleep-threshold` | 100 | Frames of closed eyes before alarm |
| `--alarm-beeps` | 3 | Number of beeps per alarm |
| `--camera` | 0 | Camera index (use 1 for external camera) |

Example — stricter detection with more beeps:

```bash
python drowsiness_detector.py --no-display --ear-threshold 0.15 --alarm-beeps 5
```

Here `--ear-threshold 0.15` means the alarm triggers at a tighter eye-closure level (default is 0.20), so brief squints or dim lighting are less likely to set it off. Combined with `--no-display` the script runs silently in the background, and `--alarm-beeps 5` plays five beeps per alarm instead of three for a louder wake-up call.
