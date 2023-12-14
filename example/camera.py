import cv2
from zephyr import Stream

if __name__ == "__main__":
    stream = Stream(
        url="rtsp://localhost:8554/test", resolution=(1280, 720), fps=30, bitrate="2M"
    )

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        stream.send(frame)
