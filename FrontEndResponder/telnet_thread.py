import threading  # https://docs.python.org/3/library/threading.html
import socket  # https://docs.python.org/3/library/socket.html
import select  # https://docs.python.org/3/library/select.html
import logging

import byte_parser
from Profiles.ProfileLogic import ProfileLogic


# Options: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.hald001/telcmds.htm
# Options: https://www.iana.org/assignments/telnet-options/telnet-options.xhtml
# Commands: https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html
# RFC: https://tools.ietf.org/html/rfc854
# RFC Options: https://tools.ietf.org/html/rfc1060#page-51


class TelnetThread(threading.Thread):
    """Defines a Thread that includes variables and functions needed for Telnet Functionality."""

    def __init__(self, client: socket, database: ProfileLogic):
        """Extend the Thread class with variables to keep track of the client/socket connection
        if it should close, and what data has been received so far."""
        threading.Thread.__init__(self)
        self.conn = client
        self.database = database
        self.client_ip = client.getpeername()[0]
        self.alive = True  # Ensures we can close the thread in a friendly way.
        self.history = bytearray()
        self.profile = {}
        self.welcome_send = False

    def run(self):
        """When the thread is started it will output some logging information and start the telnet_thread."""
        logging.info(f"Incoming connection received from: {self.client_ip}.")
        self.set_random_profile()
        self.telnet_thread()
        logging.info(f"Connection closed from: {self.client_ip}")

    def set_random_profile(self):
        self.profile = self.database.get_random_profile()
        profile_id = self.profile.get("_id")
        logging.info(f"Requesting random profile from database. Got: {profile_id}")

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
                commands, text = byte_parser.parse_buffer(buffer, self.client_ip)
                self.process_commands(commands)

                # DEBUG
                # print(self.history)
                print(commands)
                print(text)
                # DEBUG

            if not self.welcome_send:
                # self.send_to_client(str.encode(self.profile.get('welcome')))
                self.welcome_send = True
        self.conn.close()

    def respond_to_option(self, command, accept=True):
        """Reponds to an option that is retrieved from the client.
        By default accepts the option, otherwise checks what is defined in the database profile."""
        if accept:
            option_type = command[0]
            if option_type == 251:  # I Will -> You Do
                # Do not accept linemode
                if command[1] == 34:
                    self.send_to_client(bytearray([255, 254, command[1]]))
                else:
                    self.send_to_client(bytearray([255, 253, command[1]]))
            if option_type == 252:  # I Wont -> You Dont
                self.send_to_client(bytearray([255, 254, command[1]]))
            if option_type == 253:  # You Do -> I Will
                self.send_to_client(bytearray([255, 251, command[1]]))
            if option_type == 254:  # You Dont -> I wont
                self.send_to_client(bytearray([255, 252, command[1]]))
        else:  # TODO implement db.profile.options responses
            print(2)

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

    def terminate_thread(self):
        logging.info(f"{self.client_ip} terminated connection")
        self.alive = False

    def process_commands(self, commands):
        """Process the retrieved commands by returning options or taking other actions."""
        for command in commands:
            if command[0] > 250:  # Telnet option
                self.respond_to_option(command)
            else:
                for byte in command:
                    if byte == 244:  # Interrupt Process
                        self.terminate_thread()
                    if byte == 250:
                        self.sub_negotiation(command)
                        break

    def sub_negotiation(self, command):
        """Open Sub negotiation"""
        if len(command) > 2:
            """Negotiate About Window Size"""
            if command[1] == 31:
                pass
