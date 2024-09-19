from fer import FER
from fer.utils import draw_annotations

import cv2
import json
import base64

import asyncio
from websockets.asyncio.server import serve


def frame_to_base64(frame):
    """
    Convert frame to transmittable format
    """
    _, buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
    frame_base64 = base64.b64encode(buffer)
    return frame_base64.decode('utf-8') 


async def detect_emotions(websocket, device=0):
    """
    Detect emotions and distribute to websocket
    """
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(device)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        emotions = detector.detect_emotions(frame)
        frame = draw_annotations(frame, emotions)

        data = {
            "emotions": emotions, 
            "frame": frame_to_base64(frame)
        }
        
        await websocket.send(json.dumps(data))

        """
        !important
        Allow other async tasks to kick in
        """
        await asyncio.sleep(0)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()


async def main():
    async with serve(detect_emotions, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  

asyncio.run(main())
