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


def divide_frame_into_regions(frame: np.ndarray, n: int = 6) -> Dict:
    """
    Frame is divided into nxn parts (regions) with (i, j) indexing:
    (n, 1) … (n, n)
    …   …   …   …
    (1, 1) … (1, n)

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
    # FIXME: This function does not work properly
    """
    Defines region in which the object is located.
    :param frame: frame in which to calculate
    :param center: center of the object
    :return: tuple(i, j, n)
    """
    n = regions["n"]
    w, h = regions["frame_size"]
    x, y = center
    region_width, region_height = regions[("w", "h")]
    i = int(x // region_width)
    j = int(y // region_height)
    return (i, j, n)


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


# ~~~~~~~~~~ Frame processing ~~~~~~~~~~
def get_frame_size(frame: np.ndarray) -> Tuple[int, int]:
    return (frame.shape[1], frame.shape[0])


def resize_frame(frame: np.ndarray, scale: float = 0.5) -> np.ndarray:
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def get_gray_frame(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# ~~~~~~~~~~ Drawings ~~~~~~~~~~~
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


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    frame = cap.read()[1]
    print(divide_frame_into_regions(frame))
    print(divide_frame_into_regions(frame)[(1, 1)])
