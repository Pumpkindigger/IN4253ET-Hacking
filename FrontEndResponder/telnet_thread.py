import threading  # https://docs.python.org/3/library/threading.html
import socket  # https://docs.python.org/3/library/socket.html
import select  # https://docs.python.org/3/library/select.html
import logging
import byte_parser

# Options: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.hald001/telcmds.htm
# Options: https://www.iana.org/assignments/telnet-options/telnet-options.xhtml
# RFC: https://tools.ietf.org/html/rfc854


class TelnetThread(threading.Thread):
    """Defines a Thread that includes variables and functions needed for Telnet Functionality."""

    def __init__(self, client: socket):
        """Extend the Thread class with variables to keep track of the client/socket connection
        if it should close, and what data has been received so far."""
        threading.Thread.__init__(self)
        self.conn = client
        self.client_ip = client.getpeername()[0]
        self.alive = True  # Ensures we can close the thread in a friendly way.
        self.history = bytearray()

    def run(self):
        """When the thread is started it will output some logging information and start the telnet_thread."""
        logging.info(f"Incoming connection received from: {self.client_ip}.")
        self.telnet_thread()
        logging.info(f"Connection closed from: {self.client_ip}")

    def telnet_thread(self):
        """Handling of incoming/outgoing bytes."""
        while self.alive:
            ready = select.select([self.conn], [], [], 5)
            if ready[0]:
                buffer = self.conn.recv(4096)

                # Closes socket if the client suddenly disappeared.
                if not len(buffer):
                    logging.warning(f"Connection unexpectedly broken from: {self.client_ip}")
                    self.alive = False
                    continue

                self.history += buffer
                print(buffer)
                byte_parser.parse_string(buffer, self.client_ip)
                print(self.history)
        self.conn.close()

    def send_to_client(self, data: bytes):
        """Sends data to the client via socket."""
        total_bytes = len(data)
        total_sent = 0
        try:
            while total_sent < total_bytes:
                bytes_send = self.conn.send(data[total_sent:])
                if not bytes_send:
                    raise BrokenPipeError("Socket connection broken.")
                total_sent += bytes_send
        except BrokenPipeError:
            logging.warning(f"Connection unexpectedly broken from: {self.client_ip}")
            self.alive = False
