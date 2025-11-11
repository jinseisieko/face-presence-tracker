import cv2
import time
import json
import requests
import base64
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | processor | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("processor")

SEND_INTERVAL = 1
FRAME_WIDTH, FRAME_HEIGHT = 320, 240

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_send_time = 0


logger.info("Processor started. Sending frames to analyzer...")

def detectFaces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    has_face = len(faces) > 0

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return has_face

while True:
    ret, frame = cap.read()
    if not ret:
        logger.warning("Failed to grab frame")
        time.sleep(1)
        continue

    has_face = detectFaces(frame)

    current_time = time.time()
    if current_time - last_send_time >= SEND_INTERVAL:
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        frame_b64 = base64.b64encode(buffer).decode('utf-8')

        payload = {
            "timestamp": current_time,
            "has_face": has_face,
            "frame_b64": frame_b64
        }

        try:
            response = requests.post(
                "http://analyzer:5000/frame",
                json=payload,
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Frame sent | has_face: {has_face}")
            else:
                logger.warning(f"Analyzer error: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send frame: {e}")

        last_send_time = current_time

    time.sleep(0.01)  

cap.release()