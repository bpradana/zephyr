import logging
import multiprocessing as mp
from urllib.parse import urlparse


from zephyr.client.reconnect import Reconnect


class Client:
    RESET_REQUEST = 0
    FRAME_REQUEST = 1
    CLOSE_REQUEST = 2

    def __init__(self, url):
        # load pipe for data transmission to the process
        self.parent_conn, self.child_conn = mp.Pipe()

        # load parameters
        self.url = url

        # start process
        self._start()

    def _start(self):
        self.process = mp.Process(target=self._update, args=(self.child_conn,))
        self.process.daemon = True
        self.process.start()

    def release(self):
        self.parent_conn.send(Client.CLOSE_REQUEST)
        self.process.join()

    def _update(self, child_connection):
        cap = Reconnect(self.url)
        run = True

        while run:
            # grab frames from the buffer
            _ = cap.grab()

            # receive command data
            command_data = child_connection.recv()

            # if frame requested send frame to main process
            if command_data == Client.FRAME_REQUEST:
                _, frame = cap.retrieve()
                child_connection.send(frame)

            # if close requested release camera and stop loop
            if command_data == Client.CLOSE_REQUEST:
                # if close requested
                cap.release()
                run = False

        logging.info(
            f"camera {urlparse(self.url).hostname} connection closed",
        )

        child_connection.close()

    def read(self):
        # send request
        self.parent_conn.send(Client.FRAME_REQUEST)
        frame = self.parent_conn.recv()

        # reset request
        self.parent_conn.send(Client.RESET_REQUEST)

        return None, frame
