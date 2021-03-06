# Requires administrator privileges to bind to a port.
import socket  # https://docs.python.org/3/library/socket.html#
import threading  # https://docs.python.org/3/library/threading.html
import logging
import os
import time
import sys

from FrontEndResponder.telnet_thread import TelnetThread
from Profiles.ProfileLogic import ProfileLogic
from Profiles.DatabaseConnection import DatabaseConnection


def init_logging():
    """Initializes logging to file and stdout and sets configuration and format settings."""
    if not os.path.exists('../logs'):
        os.mkdir("../logs")
    file_handler = logging.FileHandler(filename='../logs/' + str(int(time.time())) + '.log')
    stdout_handler = logging.StreamHandler(sys.stdout)

    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=[file_handler, stdout_handler]
    )


def init_socket():
    """Initializes listening on a socket with the correct settings so it can be reused."""
    listen_port = 23
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                        1)  # Ensures socket is reusable when this program closes.
    listener.bind(('', listen_port))
    listener.listen()
    logging.info(f"FrontEndResponder is listening on port {listen_port}.")
    return listener


def init_database_conn():
    return ProfileLogic(DatabaseConnection("myFirstDatabase", "profiles"))


def handle_incoming_connections(listener):
    """Endless loop to automatically accept the connection and create a TelnetThread."""
    global database
    try:
        while True:
            client, address = listener.accept()
            TelnetThread(client).start()
    except KeyboardInterrupt:
        logging.info("Closing FrontEndResponder...")
        listener.shutdown(1)
        listener.close()
        database.dbcon.client.close()

        # Make sure to cleanly exit the running Telnet connections.
        for thread in threading.enumerate():
            if "Thread-" in thread.name:
                thread.alive = False
                thread.join()


init_logging()
database = init_database_conn()
handle_incoming_connections(init_socket())
