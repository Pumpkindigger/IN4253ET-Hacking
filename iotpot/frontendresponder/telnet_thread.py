import threading  # https://docs.python.org/3/library/threading.html
import socket  # https://docs.python.org/3/library/socket.html
import select  # https://docs.python.org/3/library/select.html
import logging

from frontendresponder.byte_parser import ByteParser
from database.logging_logic import LoggingLogic
from database.profile_logic import ProfileLogic
from manager.vm import VM


# Options: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.hald001/telcmds.htm
# Options: https://www.iana.org/assignments/telnet-options/telnet-options.xhtml
# Commands: https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html
# RFC: https://tools.ietf.org/html/rfc854
# RFC Options: https://tools.ietf.org/html/rfc1060#page-51


class TelnetThread(threading.Thread):
    """Defines a Thread that includes variables and functions needed for Telnet Functionality."""

    def __init__(self, client: socket, database_profile: ProfileLogic, database_logging: LoggingLogic, vm_connection: VM):
        """Extend the Thread class with variables to keep track of the client/socket connection
        if it should close, and what data has been received so far."""
        threading.Thread.__init__(self)
        self.conn = client
        self.database_profile = database_profile
        self.database_logging = database_logging
        self.client_ip = client.getpeername()[0]
        self.alive = True  # Ensures we can close the thread in a friendly way.
        self.history = bytearray()
        self.profile = {}
        self.welcome_send = False
        self.logged_in = False
        self.login_username = None
        self.login_counter = 0
        self.vm_connection = vm_connection

    def run(self):
        """When the thread is started it will output some logging information and start the telnet_thread."""
        logging.info(f"Incoming connection received from: {self.client_ip}.")
        logging.info(f"For {self.client_ip}: Using {self.vm_connection.get_architecture()} architecture.")
        self.vm_connection.start_session()
        self.set_random_profile()
        self.telnet_thread()

        logging.info(f"Connection closed from: {self.client_ip}")
        logging_id = self.database_logging.insert_log(self.profile.get("_id"), self.client_ip, self.history, self.vm_connection.get_architecture())
        logging.info(f"Session from {self.client_ip} is logged to MongoDB with id: {logging_id}")
        self.vm_connection.current_users -= 1

    def set_random_profile(self):
        self.profile = self.database_profile.get_random_profile()
        profile_id = self.profile.get("_id")
        logging.info(f"For {self.client_ip}: Requesting random profile from database. Got: {profile_id}")

    def login(self, login_text):
        if self.login_username is None:
            self.login_username = login_text
            #self.send_to_client(b'\xff\xfb\x01')
            self.send_to_client(str.encode("Password: "))  # TODO implement disabling echo so password won't be seen.
        else:
            #self.send_to_client(b'\xff\xfe\x01')
            logging.info(f"For {self.client_ip}: Tried to login with {self.login_username}:{login_text}")
            authentication_type = self.profile.get("Authentication")
            if type(authentication_type) is str and authentication_type == "Always":  # Always accept
                self.send_to_client(str.encode("Welcome! \n"))
                self.logged_in = True
            elif type(authentication_type) is int:  # Accept after x tries
                self.login_counter += 1
                if self.login_counter > authentication_type:
                    self.send_to_client(str.encode("Welcome! \n"))
                    self.logged_in = True
                else:
                    self.login_username = None
                    self.send_to_client(str.encode("Invalid login...\nLogin: "))
            elif type(authentication_type) is dict:  # Accept for specific username/password combinations
                required_password = authentication_type.get(self.login_username)
                if required_password is not None and required_password == login_text:
                    self.send_to_client(str.encode("Welcome! \n"))
                    self.logged_in = True
                else:
                    self.login_username = None
                    self.send_to_client(str.encode("Invalid login...\nLogin: "))
            else:  # Never accept
                self.login_username = None
                self.send_to_client(str.encode("Invalid login...\nLogin: "))

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
                commands, text = ByteParser.parse_buffer(buffer, self.client_ip)
                self.process_commands(commands)

                if self.alive:  # Extra check because it could be that the user has just sent a close connection command.
                    if len(text) > 0 and not self.logged_in:
                        self.login(text)
                    elif self.logged_in:
                        logging.info(f"For {self.client_ip}: Run command \"{text}\"")
                        self.send_to_client(self.vm_connection.run_command(text))
            if not self.welcome_send:
                self.send_to_client(str.encode(bytes(self.profile.get("Welcome"), "utf-8").decode("unicode_escape")))
                self.welcome_send = True
        self.conn.close()

    def respond_to_option(self, command, accept=True):
        """Reponds to an option that is retrieved from the client.
        By default accepts the option, otherwise checks what is defined in the database profile."""
        if accept:
            option_type = command[0]
            if option_type == 251:  # I Will -> You Do
                if command[1] == 34 or command[1] == 33:  # Required to disable Linemode or Remote Flow Control Option.
                    self.send_to_client(bytearray([255, 252, command[1]]))
                else:
                    self.send_to_client(bytearray([255, 253, command[1]]))
            if option_type == 252:  # I Wont -> You Dont
                self.send_to_client(bytearray([255, 254, command[1]]))
            if option_type == 253:  # You Do -> I Will
                self.send_to_client(bytearray([255, 251, command[1]]))
            if option_type == 254:  # You Dont -> I Wont
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
        """Open Sub negotiation, when SB (Code 250) gets called this function responds to the sub negotiation"""
        if len(command) > 2:
            """Negotiate About Window Size, accept the clients new window size"""
            if command[1] == 31:
                pass
