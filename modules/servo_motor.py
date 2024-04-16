"""
This module contains the Servomotor class, which is used to drive a servomotor with camera.
"""

from typing import Tuple


class Servomotor:
    def __init__(self):
        pass

    def calculate_velocity(self, position: Tuple[int, int, int]) -> Tuple[int, int]:
        """
        Calculates abstract velocity for servo motor.
        In essence, the center of coordinates is transferred to center of frame.
        :param position: tuple(i, j, n), where i, j - index of the region,
        n - quontity of regions by width.
        :return: tuple(x, y)
        """
        x, y, n = position
        half = n / 2
        if x <= half:
            x = x - (half + 1)
        else:
            x = x - half
        if y <= half:
            y = y - (half + 1)
        else:
            y = y - half
        return (int(x), int(y))
