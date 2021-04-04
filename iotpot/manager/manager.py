from manager.vm import VM
import time
import logging
import threading
import subprocess
import telnetlib


class Manager:
    def __init__(self):
        self.vm_list = []
        self.thread = self.start_thread()
        self.init_vms()

    def init_vms(self):
        """Initializes all configured architectures and store them in the class list of VMs"""
        # The amount of supported architectures is currently hardcoded to 3.
        architectures = 3
        for i in range(architectures):
            self.init_vm(i)

    def init_vm(self, id):
        """Initialize a telnet connection to a VM if this VM is currently not in the VM list."""
        for vm in self.vm_list:
            if vm.id == id:
                logging.warning(f"Tried to initialize the {vm.get_architecture()} QEMU instance while it already exists.")
                return
        self.vm_list.append(VM(id))

    def run_command(self, tn, command):
        #copied from vm for testing purposes
        tn.write(str.encode(command + "\n"))
        time.sleep(1)
        response = tn.read_very_eager()
        response = response[len(command)+2:]  # remove the first line because it echoes the command
        return response

    def restart_vm(self, vm):
        logging.info(f"Refreshing the {vm.get_architecture()} architecture QEMU instance because it's old and unused.")
        id = vm.id

        # this option does not properly close telnet connection with earlier qemu instance
        # vm.run_command("poweroff")

        vm.close_telnet_connection()

        # this option gives broken pipeline error, not sure why
        tn = telnetlib.Telnet("127.0.0.1", vm.id+45454)
        response = self.run_command(tn, "quit")
        tn.close()
        time.sleep(30)
        
        self.vm_list.remove(vm)

        bashCmd = ["sh", "/iotpot/manager/restart.sh", str(id)]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        # output, error = process.communicate()
        # logging.info(f"output of restart {output}")

        self.init_vm(id)
        return []

    def start_thread(self):
        thread = threading.Timer(60.0, self.check_status_vms)
        thread.start()
        return thread

    def check_status_vms(self):
        logging.info("Checking if any VM needs to be refreshed...")
        self.thread = self.start_thread()
        current_time = int(time.time())
        for vm in self.vm_list:
            if vm.current_users == 0 and current_time - vm.start_time > 50:
                self.restart_vm(vm)
