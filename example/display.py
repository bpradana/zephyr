import cv2
from zephyr import Client

if __name__ == "__main__":
    client = Client(url="rtsp://localhost:8554/test")

    while True:
        ret, frame = client.read()
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            client.release()
            break
