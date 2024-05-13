import sys
import serial

DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == "DEBUG":
    DEBUG = True

CAM = 1  # index number of camera

# ~~~~~~~~~ Arduino settings ~~~~~~~~~
INITIAL_X = 1400
INITIAL_Y = 1400

USB_PORT = "/dev/cu.usbserial-20"  # nix
# USB_PORT = "COM3"  # windows
usb = serial.Serial(USB_PORT, 115200)


def data_string(name: str, angle: int):
    string = "%" + name + str(angle) + "#"
    return string.encode()


usb.write(data_string("X", INITIAL_X))
usb.write(data_string("Y", INITIAL_Y))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
