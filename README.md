# Drowsiness Detector

A real-time drowsiness detection system using your webcam. It monitors your eyes and alerts you when you fall asleep, while ignoring normal blinks.

## How It Works

The script uses the **Eye Aspect Ratio (EAR)** technique with MediaPipe Face Landmarker:

1. MediaPipe detects 478 facial landmarks in real time
2. Computes EAR from 6 eye landmarks per eye — a single number that drops to ~0 when eyes close
3. **Short closure** (< 1 second) → classified as a **blink** → ignored
4. **Long closure** (>= 1 second) → classified as **drowsiness** → triggers alarm

## Prerequisites

- Python 3.8+
- A webcam
- Model file auto-downloaded on first run (`face_landmarker.task`)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python drowsiness_detector.py
```

Press `q` to quit.

### Optional arguments

```bash
python drowsiness_detector.py --ear-threshold 0.25    # lower = stricter
python drowsiness_detector.py --sleep-threshold 100    # frames before alarm
python drowsiness_detector.py --alarm-beeps 5         # more beeps per alarm
python drowsiness_detector.py --camera 1              # use second camera
```

The `face_landmarker.task` model (~4 MB) is auto-downloaded from Google servers on first run.
