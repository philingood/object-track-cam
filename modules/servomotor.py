"""
This module contains the Servomotor class, which is used to drive a servomotor
with camera.
"""

from typing import Sequence, Tuple
from cv2.typing import Rect
import logging

logging.getLogger(__name__)


class Servomotor:
    def __init__(self):
        pass

    @staticmethod
    def calculate_velocity(
        position: Tuple[int, int, int],
        central_region: Sequence[Rect],
        center_of_frame: Tuple[int, int],
    ) -> Tuple[int, int]:
        """
        Calculates abstract velocity for servo motor.
        In essence, the coordinate center is transferred to the center of
        the frame and the region index is recalculated.
        :param position: tuple(i, j, n), where i, j - index of the region
        in which center of the object is located, n - quontity of regions
        by width.
        :param central_region: coordinates of rectangle of the central region.
        :param center: tuple(x, y), where x, y - coordinates of the center of
        the object.
        :return: tuple(vx, vy)
        """
        x, y = center_of_frame
        i, j, n = position
        xcr, ycr, wcr, hcr = [a for a in central_region[0]]
        half = n // 2
        vx: int
        vy: int

        # If center of the object is in the central region
        if x in range(xcr, xcr + wcr) and y in range(ycr, ycr + hcr):
            vx = vy = 0
            return (vx, vy)

        # If center of the object is in the left half of the frame
        if i <= half:
            vx = i - (half + 1)
        # If center of the object is in the right half of the frame
        else:
            vx = i - half

        # If the center of the object is in the top half of the frame
        if j <= half:
            vy = -j + (half + 1)
        # If the center of the object is in the bottom half of the frame
        else:
            vy = -j + half
        return (vx, vy)
