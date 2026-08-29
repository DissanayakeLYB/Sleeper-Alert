import argparse
import math
import time
import sys
import os
import urllib.request
import cv2
import mediapipe as mp
import numpy as np

# ---------------------------------------------------------------------------
# Model download
# ---------------------------------------------------------------------------

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")


def ensure_model():
    """Download the face_landmarker.task model if not already present."""
    if os.path.exists(MODEL_PATH):
        print(f"[INFO] Model already exists at {MODEL_PATH}")
        return MODEL_PATH
    print(f"[INFO] Downloading face_landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")
    return MODEL_PATH


# ---------------------------------------------------------------------------
# Eye Aspect Ratio (EAR) calculation
# ---------------------------------------------------------------------------

def eye_aspect_ratio(eye):
    """
    Compute the Eye Aspect Ratio for a single eye given 6 (x, y) points.

    EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    Approximately constant when open, drops to ~0 when closed.
    """
    A = _distance(eye[1], eye[5])
    B = _distance(eye[2], eye[4])
    C = _distance(eye[0], eye[3])
    if C == 0:
        return 0.0
    return (A + B) / (2.0 * C)


def _distance(p1, p2):
    """Euclidean distance between two (x, y) points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


# ---------------------------------------------------------------------------
# Alarm
# ---------------------------------------------------------------------------

def play_alarm(num_beeps=3):
    """Play an audible alert. Cross-platform."""
    for _ in range(num_beeps):
        if sys.platform == "win32":
            try:
                import winsound
                winsound.Beep(1000, 500)
            except ImportError:
                sys.stdout.write("\a")
                sys.stdout.flush()
                time.sleep(0.5)
        elif sys.platform == "darwin":
            os.system('afplay /System/Library/Sounds/Glass.aiff &')
            time.sleep(0.5)
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.5)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Drowsiness detector using Eye Aspect Ratio (EAR)"
    )
    parser.add_argument(
        "-e", "--ear-threshold",
        type=float, default=0.2,
        help="EAR value below which eyes are considered closed (default: 0.2)",
    )
    parser.add_argument(
        "-s", "--sleep-threshold",
        type=int, default=100,
        help="Consecutive closed-eye frames before triggering alarm (default: 100)",
    )
    parser.add_argument(
        "-b", "--alarm-beeps",
        type=int, default=3,
        help="Number of alarm beeps per wake-up cycle (default: 3)",
    )
    parser.add_argument(
        "-c", "--camera",
        type=int, default=0,
        help="Camera index (default: 0)",
    )
    args = parser.parse_args()

    # --- Constants --------------------------------------------------------
    EYE_AR_THRESH = args.ear_threshold
    SLEEP_FRAMES = args.sleep_threshold

    # MediaPipe 478-point Face Landmarker landmark indices for eyes
    # Ordering: 0=inner corner, 1=top-inner, 2=top-outer, 3=outer corner,
    #           4=bottom-outer, 5=bottom-inner
    LEFT_EYE_IDX = [362, 385, 387, 263, 373, 380]
    RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]

    # --- Download model & create Face Landmarker --------------------------
    model_path = ensure_model()

    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    print("[INFO] Initializing Face Landmarker...")
    landmarker = FaceLandmarker.create_from_options(options)

    # --- Open webcam ------------------------------------------------------
    print("[INFO] Opening webcam...")
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam. Please check your camera connection.")
        landmarker.close()
        return

    time.sleep(1.0)

    closed_frames = 0
    alarm_playing = False
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_time = time.time()
    fps_count = 0
    display_fps = 0
    frame_idx = 0

    print("[INFO] Running — press 'q' to quit.")
    print(f"[INFO] EAR threshold: {EYE_AR_THRESH} | Sleep frame threshold: {SLEEP_FRAMES}")
    print()

    # --- Main loop --------------------------------------------------------
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Convert BGR (OpenCV) → RGB (MediaPipe)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # FPS counter
        fps_count += 1
        if time.time() - fps_time >= 1.0:
            display_fps = fps_count
            fps_count = 0
            fps_time = time.time()

        # Detect landmarks (VIDEO mode needs timestamp in ms)
        timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks:
            face = result.face_landmarks[0]

            def get_eye(idx_list):
                """Convert normalized landmarks to pixel coordinates."""
                return [
                    (int(face[i].x * frame_w), int(face[i].y * frame_h))
                    for i in idx_list
                ]

            left_eye = get_eye(LEFT_EYE_IDX)
            right_eye = get_eye(RIGHT_EYE_IDX)

            # Compute EAR for both eyes and average
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            # Draw eye contours for visual feedback
            left_pts = np.array(left_eye, dtype=np.int32)
            right_pts = np.array(right_eye, dtype=np.int32)
            cv2.polylines(frame, [left_pts], True, (0, 255, 0), 1)
            cv2.polylines(frame, [right_pts], True, (0, 255, 0), 1)

            # --- Drowsiness logic ---
            if ear < EYE_AR_THRESH:
                closed_frames += 1

                # Show EAR and counter
                cv2.putText(
                    frame, f"EAR: {ear:.3f}  (closed: {closed_frames}/{SLEEP_FRAMES})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2,
                )

                if closed_frames >= SLEEP_FRAMES:
                    alarm_playing = True
                    cv2.putText(
                        frame, "Wake up! You seem to be falling asleep!",
                        (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                    )
                    play_alarm(args.alarm_beeps)

            else:
                if closed_frames >= SLEEP_FRAMES:
                    print("[INFO] User woke up. Alarm stopped.")
                closed_frames = 0
                alarm_playing = False
                cv2.putText(
                    frame, f"EAR: {ear:.3f}  [EYES OPEN]",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
                )
        else:
            cv2.putText(
                frame, "No face detected — look at the camera",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2,
            )

        # Show FPS
        cv2.putText(
            frame, f"FPS: {display_fps}",
            (10, frame_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
        )

        cv2.imshow("Drowsiness Detector", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        frame_idx += 1

    # --- Cleanup ----------------------------------------------------------
    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()
    print("[INFO] Detector stopped.")


if __name__ == "__main__":
    main()
