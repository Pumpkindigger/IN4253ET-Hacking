import time
import telnetlib
import logging


class VM:
    def __init__(self, id):
        # The ports currently start at 4321 as this is hardcoded in qemu-setup.sh
        self.id = id
        self.port = 4321 + id
        self.start_time = int(time.time())
        self.telnet_connection = self.init_vm_telnet()
        self.current_users = 0

    def get_architecture(self):
        """These architectures directly correspond to the configured qemu images in qemu-setup.sh"""
        if self.id == 0:
            return "x86_64"
        elif self.id == 1:
            return "mips"
        elif self.id == 2:
            return "ARM"
        else:
            return "UNKNOWN"

    def init_vm_telnet(self):
        logging.info(f"Trying to set up a telnet connection to the {self.get_architecture()} VM...")
        return telnetlib.Telnet("127.0.0.1", self.port)

    def start_session(self):
        if self.current_users == 0:
            self.run_command("")
            self.telnet_connection.read_very_eager()  # This is done to flush the boot messages
        self.current_users += 1

    def run_command(self, command):
        self.telnet_connection.write(str.encode(command + "\n"))
        time.sleep(1)
        response = self.telnet_connection.read_very_eager()
        response = response[len(command)+2:]  # remove the first line because it echoes the command
        return response

    def close_telnet_connection(self):
        self.telnet_connection.close()
