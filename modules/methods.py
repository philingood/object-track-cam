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


