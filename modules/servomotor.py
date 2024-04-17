"""
This module contains the Servomotor class, which is used to drive a servomotor
with camera.
"""

from typing import Tuple


class Servomotor:
    def __init__(self):
        pass

    @staticmethod
    def calculate_velocity(position: Tuple[int, int, int]) -> Tuple[int, int]:
        """
        Calculates abstract velocity for servo motor.
        In essence, the coordinate center is transferred to the center of
        the frame and the region index is recalculated.
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
