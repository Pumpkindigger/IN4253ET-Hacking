# Requires administrator privileges to bind to a port.
import socket  # https://docs.python.org/3/library/socket.html#
import threading  # https://docs.python.org/3/library/threading.html

from FrontEndResponder.telnet_thread import TelnetThread

# Setup of the listener socket.
listen_port = 23
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Ensures socket is reusable when this program closes.
listener.bind(('', listen_port))
listener.listen()
print(f"FrontEndResponder is listening on port {listen_port}.")

# Endless loop to automatically accept the connection and create a TelnetThread.
try:
    while True:
        client, address = listener.accept()
        TelnetThread(client).start()
except KeyboardInterrupt:
    print("Closing FrontEndResponder...")
    listener.shutdown(1)
    listener.close()

    # Make sure to cleanly exit the running Telnet connections.
    for thread in threading.enumerate():
        if "MainThread" in thread.name:
            continue
        thread.alive = False
        thread.join()
