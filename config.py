import serial
import argparse


CAM = 1  # index number of camera


def parse_arguments():
    parser = argparse.ArgumentParser(description="Description of your script")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--no-arduino", action="store_true", help="Disable Arduino mode"
    )

    return parser.parse_args()


# ~~~~~~~~~ Arduino settings ~~~~~~~~~
INITIAL_X = 1400
INITIAL_Y = 1400


def data_string(name: str, angle: int):
    string = "%" + name + str(angle) + "#"
    return string.encode()


USB_PORT = "/dev/cu.usbserial-20"  # nix
# USB_PORT = "COM3"  # windows

if parse_arguments().no_arduino:
    usb = None
else:
    usb = serial.Serial(USB_PORT, 115200)
    usb.write(data_string("X", INITIAL_X))
    usb.write(data_string("Y", INITIAL_Y))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
