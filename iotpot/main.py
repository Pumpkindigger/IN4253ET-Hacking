# Requires administrator privileges to bind to a port.
import socket  # https://docs.python.org/3/library/socket.html#
import threading  # https://docs.python.org/3/library/threading.html
import logging
import os
import time
import sys
import random

from frontendresponder.telnet_thread import TelnetThread
from database.logging_logic import LoggingLogic
from database.profile_logic import ProfileLogic
from database.database_connection import DatabaseConnection
from manager.manager import Manager


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
    return ProfileLogic(DatabaseConnection("profileDB", "profiles")),\
           LoggingLogic(DatabaseConnection("profileDB", "logging"))


def handle_incoming_connections(listener):
    """Endless loop to automatically accept the connection and create a TelnetThread."""
    global database_profile, database_logging, vm_manager
    try:
        while True:
            client, address = listener.accept()
            vm = random.choice(vm_manager.vm_list)
            TelnetThread(client, database_profile, database_logging, vm).start()
    except KeyboardInterrupt:
        logging.info("Closing FrontEndResponder...")
        listener.shutdown(1)
        listener.close()
        database_profile.dbcon.client.close()
        vm_manager.thread.cancel()

        # Make sure to cleanly exit the running Telnet connections.
        for thread in threading.enumerate():
            if "Thread-" in thread.name:
                thread.alive = False
                thread.join()

        # Closing logging database should be last as the closing telnet threads might want to write to it.
        database_logging.dbcon.client.close()


init_logging()
database_profile, database_logging = init_database_conn()
vm_manager = Manager()
handle_incoming_connections(init_socket())
