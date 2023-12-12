import logging
import time
from urllib.parse import urlparse

import cv2
from tenacity import retry


class Reconnect:
    """
    A class for reconnecting to a camera.

    This class is used to reconnect to a camera if the connection is lost.

    Attributes:
        rtsp_url (str): The RTSP URL to connect to.
        rtsp_ip (str): The IP address of the RTSP URL.
        wait (int): The time to wait before attempting to reconnect.
        connection (cv2.VideoCapture): The connection to the camera.

    Methods:
        __init__(rtsp_url, wait=5): Initializes a Reconnect object.
        reconnect(): Reconnects to the camera.
        read(): Reads a frame from the camera connection.
        grab(): Grabs a connection and reconnects if necessary.
        retrieve(): Retrieves a frame from the connection.
        release(): Releases the connection.
    """

    def __init__(self, rtsp_url, wait=5):
        """
        Initializes a Reconnect object.

        Args:
            rtsp_url (str): The RTSP URL to connect to.
            wait (int): The time to wait before attempting to reconnect (default is 5 seconds).
        """
        self.rtsp_url = rtsp_url
        self.rtsp_ip = urlparse(rtsp_url).hostname
        self.wait = wait
        self.connection = None
        self.reconnect()

    @retry
    def reconnect(self):
        """
        Reconnects to the camera.

        This method attempts to reconnect to the camera using the provided RTSP URL.
        If the connection is successful, the camera is considered loaded.
        If the connection fails, an exception is raised and an error message is logged.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If the camera is not found or fails to load.

        """
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
        """
        Reads a frame from the camera connection.

        If the frame is not retrieved successfully, it logs a warning message
        indicating that the camera is disconnected and attempts to reconnect.

        Args:
            None

        Returns:
            Tuple[bool, Any]: A tuple containing a boolean value indicating
            whether the frame was retrieved successfully and the retrieved frame.
        """
        ret, frame = self.connection.read()  # type:ignore
        if not ret:
            logging.warning(
                f"camera {self.rtsp_ip} disconnected",
                extra={"tags": {"module": "camera"}},
            )
            self.reconnect()
        return ret, frame

    def grab(self):
        """
        Grabs a connection and reconnects if necessary.

        Args:
            None

        Returns:
            bool: True if the connection was successfully grabbed, False otherwise.
        """
        ret = self.connection.grab()  # type:ignore
        if not ret:
            self.reconnect()
        return ret

    def retrieve(self):
        """
        Retrieves a frame from the connection.

        Returns:
            ret (bool): True if the frame is successfully retrieved, False otherwise.
            frame: The retrieved frame.
        """
        ret, frame = self.connection.retrieve()  # type:ignore
        if not ret:
            self.reconnect()
        return ret, frame

    def release(self):
        """
        Releases the connection.
        """
        self.connection.release()  # type:ignore
