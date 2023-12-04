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
    CLOSE_REQUEST = np.array([0])

    def __init__(self, url, resolution, fps=30, bitrate="5M", mux_delay=0.1):
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
        self.process = mp.Process(target=self._update, args=(self.child_connection,))
        self.process.daemon = True
        self.process.start()

    def end(self):
        self.parent_connection.send(Stream.CLOSE_REQUEST)
        self.process.join()

    def _update(self, child_connection):
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
        frame = cv2.resize(frame, self.resolution)
        self.parent_connection.send(frame)
