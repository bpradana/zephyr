import logging
import multiprocessing as mp
from urllib.parse import urlparse


from zephyr.client.reconnect import Reconnect


class Client:
    """
    A class for receiving frames from a URL.

    Attributes:
        RESET_REQUEST (int): A constant representing a reset request.
        FRAME_REQUEST (int): A constant representing a frame request.
        CLOSE_REQUEST (int): A constant representing a close request.
        url (str): The URL of the client.
        parent_conn (multiprocessing.connection.Connection): The parent connection.
        child_conn (multiprocessing.connection.Connection): The child connection.
        process (multiprocessing.Process): The process for updating the client.

    Methods:
        __init__(url): Initializes a new instance of the Client class.
        _start(): Starts the process for updating the client.
        _update(child_connection): Updates the client by grabbing frames from the buffer, receiving command data, and sending frames to the main process if requested.
        release(): Sends a close request to the parent connection and joins the process.
        read(): Sends a request to the parent process to retrieve a frame, resets the request, and returns the frame.
    """

    RESET_REQUEST = 0
    FRAME_REQUEST = 1
    CLOSE_REQUEST = 2

    def __init__(self, url):
        """
        Initializes a new instance of the Client class.

        Args:
            url (str): The URL of the client.

        Returns:
            None
        """
        # load pipe for data transmission to the process
        self.parent_conn, self.child_conn = mp.Pipe()

        # load parameters
        self.url = url

        # start process
        self._start()

    def _start(self):
        """
        Starts the process for updating the client.

        Args:
            None

        Returns:
            None
        """
        self.process = mp.Process(target=self._update, args=(self.child_conn,))
        self.process.daemon = True
        self.process.start()

    def _update(self, child_connection):
        """
        Updates the client by grabbing frames from the buffer, receiving command data,
        and sending frames to the main process if requested.

        Args:
            child_connection: The connection to the child process.

        Returns:
            None
        """
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

    def release(self):
        """
        Sends a close request to the parent connection and joins the process.

        Args:
            None

        Returns:
            None
        """
        self.parent_conn.send(Client.CLOSE_REQUEST)
        self.process.join()

    def read(self):
        """
        Sends a request to the parent process to retrieve a frame,
        resets the request, and returns the frame.

        Args:
            None

        Returns:
            tuple: A tuple containing None as the first element and the retrieved frame as the second element.
        """
        # send request
        self.parent_conn.send(Client.FRAME_REQUEST)
        frame = self.parent_conn.recv()

        # reset request
        self.parent_conn.send(Client.RESET_REQUEST)

        return None, frame
