import cv2
from cv2.typing import Rect
from typing import Dict, Tuple, Sequence
import numpy as np


# ~~~~~~~~~~ Detectors ~~~~~~~~~~
def detect_face(
    frame: np.ndarray, faces: cv2.CascadeClassifier
) -> Tuple[bool, Sequence[Rect]]:
    """
    Detects faces in the frame.
    :param frame: frame in which to detect
    :param faces: pre-trained classifier of faces
    :return: tuple(bool, List)
    """
    face = faces.detectMultiScale(frame, scaleFactor=2.1, minNeighbors=2)
    success = True
    if len(face) == 0:
        success = False
    return (success, face)


def get_box_center(rect: Sequence[Rect]) -> Tuple[int, int]:
    x, y, w, h = rect[0][0], rect[0][1], rect[0][2], rect[0][3]
    cx: int = x + w // 2
    cy: int = y + h // 2
    return (cx, cy)


def calculate_velocity(position: Tuple[int, int, int]) -> Tuple[int, int]:
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
