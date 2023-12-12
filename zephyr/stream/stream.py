import multiprocessing as mp
import subprocess as sp
import numpy as np

import cv2

from zephyr.wrapper.constants import (
    bitstream_filter,
    codec,
    pixel_format,
    preset,
    transport,
    video_format,
)
from zephyr.wrapper.ffmpeg import FFMPEG


class Stream:
    """
    A class for streaming frames to a URL.

    Attributes:
        CLOSE_REQUEST (numpy.ndarray): A numpy array representing a close request.

    Methods:
        __init__(url, resolution, fps=30, bitrate="5M", mux_delay=0.1): Initialize the Stream object.
        _start(): Starts the process for updating the stream.
        _update(child_connection): Update the stream by continuously receiving frames from the child connection and sending them to the input of the subprocess.
        send(frame): Sends a frame to the parent connection after resizing it.
        end(): Sends a close request to the parent connection and waits for the process to join.

    Examples:
        ```python
        import cv2
        from zephyr import Stream

        stream = Stream(
            url="rtsp://localhost:8554/test",
            resolution=(1280, 720),
            fps=30,
            bitrate="2M"
        )

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            stream.send(frame)

        stream.end()
        cap.release()
        ```
    """

    CLOSE_REQUEST = np.array([0])

    def __init__(self, url, resolution, fps=30, bitrate="5M", mux_delay=0.1):
        """
        Initialize the Stream object.

        Args:
            url (str): The URL where the stream will be sent.
            resolution (tuple): The resolution of the stream in the format (width, height).
            fps (int, optional): The frames per second of the stream. Defaults to 30.
            bitrate (str, optional): The bitrate of the stream. Defaults to "5M".
            mux_delay (float, optional): The mux delay of the stream. Defaults to 0.1.

        Returns:
            None
        """
        # load pipe for data transmission to the process
        self.parent_connection, self.child_connection = mp.Pipe()

        # load parameters
        self.url = url
        self.resolution = resolution
        self.fps = fps
        self.bitrate = bitrate
        self.mux_delay = mux_delay
        self.command = (
            FFMPEG()
            .read()
            .overwrite()
            .video_format(video_format.RAW_VIDEO)
            .video_codec(codec.RAW_VIDEO)
            .pixel_format(pixel_format.BGR24)
            .resolution(self.resolution)
            .fps(self.fps)
            .input("-")
            .codec(codec.LIBX264)
            .preset(preset.ULTRAFAST)
            .video_format(video_format.RTSP)
            .rtsp_transport(transport.TCP)
            .muxdelay(self.mux_delay)
            .bitstream_filter(bitstream_filter.DUMP_EXTRA)
            .bitrate(self.bitrate)
            .output(self.url)
            .build()
        )

        # start process
        self._start()

    def _start(self):
        """
        Starts the process for updating the stream.

        Args:
            None

        Returns:
            None
        """
        self.process = mp.Process(target=self._update, args=(self.child_connection,))
        self.process.daemon = True
        self.process.start()

    def _update(self, child_connection):
        """
        Update the stream by continuously receiving frames from the child connection
        and sending them to the input of the subprocess.

        Args:
            child_connection (multiprocessing.Connection): The connection to receive frames from.

        Returns:
            None
        """
        pipe = sp.Popen(self.command, stdin=sp.PIPE)
        run = True

        while run:
            frame = child_connection.recv()
            last_frame = frame

            if frame is None:
                frame = last_frame
            if pipe.stdin is not None:
                pipe.stdin.write(frame.tobytes())

            if np.array_equal(frame, Stream.CLOSE_REQUEST):
                run = False

    def send(self, frame):
        """
        Sends a frame to the parent connection after resizing it.

        Args:
            frame: The frame to be sent.

        Returns:
            None
        """
        frame = cv2.resize(frame, self.resolution)
        self.parent_connection.send(frame)

    def end(self):
        """
        Sends a close request to the parent connection and waits for the process to join.

        Args:
            None

        Returns:
            None
        """
        self.parent_connection.send(Stream.CLOSE_REQUEST)
        self.process.join()
