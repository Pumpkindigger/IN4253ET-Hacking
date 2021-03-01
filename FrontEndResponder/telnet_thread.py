import threading  # https://docs.python.org/3/library/threading.html
import socket  # https://docs.python.org/3/library/socket.html
import select  # https://docs.python.org/3/library/select.html
import byte_parser
# Options: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.hald001/telcmds.htm
# Options: https://www.iana.org/assignments/telnet-options/telnet-options.xhtml
# RFC: https://tools.ietf.org/html/rfc854


class TelnetThread(threading.Thread):
    """Defines a Thread that includes variables and functions needed for Telnet Functionality."""

    def __init__(self, client: socket):
        threading.Thread.__init__(self)
        self.conn = client
        self.alive = True  # Ensures we can close the thread in a friendly way.
        self.history = bytearray()

    def run(self):
        client_ip = self.conn.getpeername()[0]
        print(f"Incoming connection received from: {client_ip}.")
        self.telnet_thread()
        print(f"Connection closed from: {client_ip}")

    def telnet_thread(self):
        while self.alive:
            ready = select.select([self.conn], [], [], 5)
            if ready[0]:
                buffer = self.conn.recv(4096)
                self.history += buffer
                print(buffer)
                byte_parser.ByteParser.parse_string(self,buffer)
                print(self.history)
        self.conn.close()


