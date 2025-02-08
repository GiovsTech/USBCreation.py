import os
from sys import platform
import tempfile
import parted
from glob import glob


class USB():
    def __init__(self, path):
        self.path = path

    @property
    def partition_names(self):
        names = glob("{}[0-9]*".format(self.path))
        return names

    def partition(self):
        device = parted.getDevice(self.path)
        disk = parted.freshDisk(device, "msdos")
        geometry = parted.Geometry(
            device=device, start=1, length=device.getLength() - 1
        )
        filesystem = parted.FileSystem(type="fat32", geometry=geometry)
        partition = parted.Partition(
            disk=disk, type=parted.PARTITION_NORMAL, fs=filesystem, geometry=geometry
        )
        disk.addPartition(
            partition=partition, constraint=device.optimalAlignedConstraint
        )
        partition.setFlag(parted.PARTITION_BOOT)
        disk.commit()

    def wipe_dev(self, dev_path):
        with open(dev_path, "wb") as p:
            p.write(bytearray(1024))

    def wipe(self):
        for partition in self.partition_names:
            self.wipe_dev(partition)
        self.wipe_dev(self.path)

class ISO():
    def __init__(self, image):
        self.os = platform
        self.iso_path = image

    def write(self, disk, block_size=410241024):
        iso_size = os.path.getsize(self.iso_path)
        bytes_written = 0
        if self.os == "linux" or self.os == "linux2" or self.os == "darwin":
            with open(self.iso_path, "rb") as inp:
                with open(disk, "wb", buffering=0) as out:
                    while True:
                        data = inp.read(block_size)
                        if not data:
                            break
                        out.write(data)
                        bytes_written += len(data)

                        progress = (bytes_written / iso_size) * 100
                        print(f"\rProgress: {progress:5.2f}%", end='', flush=True)

                    out.flush()
                    os.fsync(out.fileno())

if __name__ == "__main__":
    disk = "/dev/sde"
    a = USB(disk)
    a.wipe()
    a.partition()

    iso_file= "/home/giovs/Gianni/VM/ISO/debian-12.9.0-amd64-netinst.iso"
    b = ISO(iso_file)
    b.write(disk)
