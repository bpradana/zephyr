import logging
import time
from urllib.parse import urlparse

import cv2
from tenacity import retry


class Reconnect:
    def __init__(self, rtsp_url, wait=5):
        self.rtsp_url = rtsp_url
        self.rtsp_ip = urlparse(rtsp_url).hostname
        self.wait = wait
        self.connection = None
        self.reconnect()

    @retry
    def reconnect(self):
        try:
            logging.info(
                f"camera {self.rtsp_ip} loading", extra={"tags": {"module": "camera"}}
            )
            self.connection = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            if not self.connection.isOpened():
                raise Exception("camera not found")
            logging.info(
                f"camera {self.rtsp_ip} loaded", extra={"tags": {"module": "camera"}}
            )
        except Exception as e:
            logging.error(
                f"camera {self.rtsp_ip} failed to load, error: {e}",
                extra={"tags": {"module": "camera"}},
            )
            time.sleep(self.wait)

    def read(self):
        ret, frame = self.connection.read()  # type:ignore
        if not ret:
            logging.warning(
                f"camera {self.rtsp_ip} disconnected",
                extra={"tags": {"module": "camera"}},
            )
            self.reconnect()
        return ret, frame

    def grab(self):
        ret = self.connection.grab()  # type:ignore
        if not ret:
            self.reconnect()
        return ret

    def retrieve(self):
        ret, frame = self.connection.retrieve()  # type:ignore
        if not ret:
            self.reconnect()
        return ret, frame

    def release(self):
        self.connection.release()  # type:ignore
