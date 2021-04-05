from manager.vm import VM
import time
import logging
import threading
import subprocess


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

    def restart_vm(self, vm):
        logging.info(f"Refreshing the {vm.get_architecture()} architecture QEMU instance because it's old and unused.")
        vm.close_telnet_connection()
        self.vm_list.remove(vm)
        subprocess.run(["/qemu-restart-a-vm.sh", str(vm.id)], capture_output=True)
        self.init_vm(vm.id)

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
