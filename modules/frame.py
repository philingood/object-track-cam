"""
Frame processing module
"""

from typing import Dict, Tuple
from cv2 import VideoCapture

from cv2 import resize, cvtColor, COLOR_BGR2GRAY, INTER_AREA
import numpy as np


def get_frame_size(frame: np.ndarray) -> Tuple[int, int]:
    return (frame.shape[1], frame.shape[0])


def resize_frame(frame: np.ndarray, scale: float = 0.5) -> np.ndarray:
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return resize(frame, (w, h), interpolation=INTER_AREA)


def get_gray_frame(frame: np.ndarray) -> np.ndarray:
    return cvtColor(frame, COLOR_BGR2GRAY)


def get_frame(cap: VideoCapture) -> Tuple:
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.
    :param cap: cv2.VideoCapture
    :return: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = resize_frame(frame, scale=0.8)
    return (frame, get_gray_frame(frame))


def divide_frame_into_regions(frame: np.ndarray, n: int = 6) -> Dict:
    """
    Frame is divided into nxn parts (regions) with (i, j) indexing:
    (1, 1) … (n, 1)
    …   …   …   …
    (n, 1) … (n, n)

    :param frame: frame which to divide
    :param n: number of regions by width
    :return: dict of regions
    """
    w, h = get_frame_size(frame)
    region_width = w // n
    region_height = h // n
    regions = {}
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x = 0 + (i - 1) * region_width
            y = 0 + (j - 1) * region_height
            regions[(i, j)] = [x, y, region_width, region_height]
    regions[("w", "h")] = [region_width, region_height]
    regions["n"] = n
    regions["frame_size"] = (w, h)
    return regions


def define_region(
    center: Tuple[int, int],
    regions: Dict,
) -> Tuple[int, int, int]:
    """
    Defines region in which the object is located.
    :param frame: frame in which to calculate
    :param center: center of the object
    :return: tuple(i, j, n)
    """
    n = regions["n"]
    x, y = center
    region_width, region_height = regions[("w", "h")]
    i = int((x + region_width) / region_width)
    j = int((y + region_height) / region_height)
    return (i, j, n)


def central_region(frame: np.ndarray) -> np.ndarray:
    """
    Returns central region in which the abstract coordinates of center
    of the object will be zero.
    """
    cx, cy = (frame.shape[1] // 2, frame.shape[0] // 2)
    x = cx - (frame.shape[1] // 12)
    y = cy - (frame.shape[0] // 12)
    w = frame.shape[1] // 6
    h = frame.shape[0] // 6
    return np.array([[x, y, w, h]])


if __name__ == "__main__":
    import cv2
    import keys
    from draw import draw_rect

    key = keys.Keys()
    cam = cv2.VideoCapture(0)

    while True:
        _, frame = cam.read()
        frame = draw_rect(frame, central_region(frame))

        cv2.imshow("FRAME", frame)

        if key.escIsPressed():
            break
