from fer import FER
from fer.utils import draw_annotations

import argparse
import cv2


def detect(device):
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(device)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame = cv2.flip(frame, 1)
        emotions = detector.detect_emotions(frame)
        frame = draw_annotations(frame, emotions)

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # TODO: Send emotions and raw frame to server

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Facial Expression Recognition")
  parser.add_argument("--device", type=int, default=0, help="Device ID to use (e.g., CPU=0, GPU=1)")
  args = parser.parse_args()

  detect(device=args.device)
