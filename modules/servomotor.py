"""
This module contains the Servomotor class, which is used to drive a servomotor
with camera.
"""

import logging
from numpy import exp
from config import usb, data_string

logging.getLogger(__name__)


class Servomotor:
    def __init__(self, name: str, correction: float = 1.0) -> None:
        self.name = name
        self.correction = correction

    def calculate_angle(self, coordinate: int, angle: int) -> int:
        if coordinate == 0:
            return angle
        else:
            # Angle in microseconds
            if angle >= 1000 and angle <= 2000:
                signe = int(coordinate / abs(coordinate))
                addition = int(
                    exp(abs(coordinate)) * self.correction / 100 / coordinate
                )
                number = int(1 + coordinate**2 * exp(1.3) / 10)
                angle -= signe * number + addition
            # Angle in degrees
            elif angle >= 0 and angle <= 180:
                angle -= 1 * coordinate
            else:
                angle = angle
            return angle

    def send_data(self, angle: int) -> None:
        """
        Sends data to arduino.
        """
        usb.write(data_string(self.name, angle))
