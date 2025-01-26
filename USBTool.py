import os
from sys import platform
import tempfile
import parted
import subprocess

class USBTool():
    def __init__(self):
        self.os = platform
        temp_dir = tempfile.TemporaryDirectory()
        ISO_DIR = os.makedirs(temp_dir.name + "/ISO")
        USB_DIR = os.makedirs(temp_dir.name + "/USB")
        self.iso_path = temp_dir.name + "/ISO"
        self.usb_path = temp_dir.name + "/USB"
    def check_file(self):
        return len(os.listdir(self.iso_path)) != 0 and len(os.listdir(self.usb_path)) != 0
    def secure_clean(self, device):
        if self.os == "linux" or "linux2":
            format_data = f"dd if=/dev/urandom of={device} bs=4096"
        elif self.os == "win32":
            pass
        elif self.os == "darwin":
            pass
        else:
            print("Your system is not supported by this program yet.")
        try:
            subprocess.run(format_data, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Something was wrong while formatting disk. Error:\n{e} ")
    def partition_disk(self, device):
        device = parted.Device(device)

    def iso_mount(self, iso_file):
        pass
    def injection(self):
        pass

if __name__ == "__main__":
    a = USBTool()