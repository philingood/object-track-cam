"""
Draw thigns on frame module
"""

import cv2
import numpy as np
from typing import Tuple, Sequence, Dict
from cv2.typing import Rect


def draw_point(
    frame: np.ndarray, point: Tuple[int, int], color: Tuple[int, int, int] = (0, 255, 0)
) -> np.ndarray:
    return cv2.circle(frame, point, 3, color, -1)


def draw_rect(
    frame: np.ndarray, rect: Sequence[Rect], color: Tuple[int, int, int] = (0, 255, 0)
) -> np.ndarray:
    """
    Draw rectangle on the frame.
    :param frame: frame in which to draw
    :param rect: list of [x, y, w, h]
    :param color: color of rectangle
    :return: frame with rectangle
    """
    rect_frame = frame
    for x, y, w, h in rect:
        rect_frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
    return rect_frame


def draw_region(
    frame: np.ndarray,
    position: Tuple[int, int, int],
    regions: Dict,
) -> np.ndarray:
    """
    Draw region in which the object is located on the frame.
    """
    i, j, n = position
    region = regions[(i, j)]
    print(region)
    return draw_rect(frame, [region])


def draw_text(
    frame: np.ndarray,
    text: str,
    color: Tuple[int, int, int] = (0, 255, 0),
    position: Tuple[int, int] = (10, 30),
) -> np.ndarray:
    return cv2.putText(
        frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA
    )


def draw_tracker_name(
    frame: np.ndarray,
    tracker_name: str,
    tracker_number: int = 1,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    """
    Draw tracker name in the corner of the frame.
    :param frame: frame in which to draw
    :param tracker_name: name of the tracker
    :param tracker_number: number of the tracker
    :param color: color of the text
    :return: frame with tracker name
    """
    scale = frame.shape[0] / 500
    return cv2.putText(
        frame, tracker_name, (10, 20 * tracker_number), 3, scale, color, 2
    )
