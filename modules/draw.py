"""
This module contains functions to draw things on frame
"""

import logging
from cv2 import circle, rectangle, putText, FONT_HERSHEY_SIMPLEX, LINE_AA
import numpy as np
from typing import Tuple, Dict, Union


def draw_point(
    frame: np.ndarray, point: Tuple[int, int], color: Tuple[int, int, int] = (0, 255, 0)
) -> np.ndarray:
    return circle(frame, point, 3, color, -1)


def draw_rect(
    frame: np.ndarray,
    rect: Union[np.ndarray, Tuple],
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    """
    Draw rectangle on the frame.
    :param frame: frame in which to draw
    :param rect: list of [x, y, w, h] or tuple of (x, y, w, h)
    :param color: color of rectangle
    :return: frame with rectangle
    """
    rect_frame = frame
    if isinstance(rect, np.ndarray):
        logging.debug("List")
        for x, y, w, h in rect:
            rect_frame = rectangle(frame, (x, y), (x + w, y + h), color, 3)
    elif isinstance(rect, Tuple):
        logging.debug("Tuple")
        x, y, w, h = tuple(map(int, rect))
        logging.debug(f"x: {x}, y: {y}, w: {w}, h: {h}")
        rect_frame = rectangle(frame, (x, y), (x + w, y + h), color, 3)
    return rect_frame


def draw_region(
    frame: np.ndarray,
    position: Tuple[int, int, int],
    regions: Dict,
) -> np.ndarray:
    """
    Draw region in which the object is located on the frame.
    """
    i, j, _ = position
    region = regions[(i, j)]
    return draw_rect(frame, np.array([region]))


def draw_text(
    frame: np.ndarray,
    text: str,
    scale: float = 1,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
    position: Tuple[int, int] = (10, 30),
) -> np.ndarray:
    return putText(
        frame,
        text,
        position,
        FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        LINE_AA,
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
    return putText(frame, tracker_name, (10, 20 * tracker_number), 3, scale, color, 2)
