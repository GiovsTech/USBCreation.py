import argparse
from USBTool import USB, ISO, glob, platform, os


## TODO: GUI DEVELOPMENT


####    ######
#         ##
#  ###    ##
#####     ##


# Parser Constants
parser = argparse.ArgumentParser(
    prog='USBCreationTool.py',
    description='A tool for creating bootable USB drives from ISO files. Run this as root',
    epilog='Use this tool to flash ISO files to USB drives.'
)

subparsers = parser.add_subparsers(dest='action', required=True)
flash_parser = subparsers.add_parser('flash', help='Flash an ISO file to a USB drive.')
flash_parser.add_argument('disk_path', type=str, help="Path to the USB disk.")
flash_parser.add_argument('iso_path', type=str, help="Path to the ISO file.")
list_parser = subparsers.add_parser('list', help='List available USB drives.')
parser.add_argument('-g', '--gui', action='store_true', help="Launch the GUI instead of CLI.")
args = parser.parse_args()


# Behaviour of the program
def flash_iso_to_usb(iso_path, usb_path):
    try:
        if os.path.exists(iso_path) and os.path.exists(usb_path):
            usb = USB(usb_path)
            iso = ISO(iso_path)
            print(" ")
            print(" Wiping your USB drive...")
            usb.wipe()
            print(" ")
            print(" Partitioning the USB drive with FAT32 filesystem...")
            usb.partition()
            print(" ")
            print(" Flashing ISO file into the USB drive...")
            print(" ")
            iso.write(usb_path)
        else:
            print(" ISO or USB PATH you provided doesn't exist. Please provide a good one.")
            return 1
    except Exception as e:
        print(f"It wasn't possibile to flash your iso image into your usb drive.\n Error: {e}")



## TODO: WINDOWS SUPPORT
def list_available_disks():
    device_pattern = "/dev/sd*" if "linux" in platform else "NONE"
    disks = glob(device_pattern)
    print(" ")
    print(" All available storage devices: ")
    print(" ")
    for d in disks:
        print(f"{d}\n")





## START OF THE PROGRAM

if args.action == "flash":
    flash_iso_to_usb(args.iso_path, args.disk_path)
elif args.action == "list":
    list_available_disks()

