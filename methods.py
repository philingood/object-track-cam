import cv2
from cv2.typing import Rect

frame = cv2.UMat


# ~~~~~~~~~~ Detectors ~~~~~~~~~~
def detect_face(frame: frame, faces) -> tuple[bool, Rect]:
    """
    Detects faces in the frame.
    :param frame: frame in which to detect
    :param faces: cv2.CascadeClassifie
    :return: tuple(bool, Rect)
    """
    face = faces.detectMultiScale(frame, scaleFactor=2.1, minNeighbors=2)
    success = True
    if len(face) == 0:
        success = False
    return (success, face)


def get_box_center(rect: Rect) -> tuple[int, int]:
    x, y, w, h = rect[0][0], rect[0][1], rect[0][2], rect[0][3]
    cx = x + w // 2
    cy = y + h // 2
    return (cx, cy)


# ~~~~~~~~~~ Frame processing ~~~~~~~~~~
def resize_frame(frame: frame, scale=0.5) -> frame:
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def get_gray_frame(frame: frame) -> frame:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# ~~~~~~~~~~ Drawings ~~~~~~~~~~~
def draw_point(
    frame: frame, point: tuple[int, int], color: tuple[int, int, int] = (0, 255, 0)
) -> frame:
    return cv2.circle(frame, point, 3, color, -1)


def draw_rect(
    frame: frame, rect: Rect, color: tuple[int, int, int] = (0, 255, 0)
) -> frame:
    """
    Draw rectangle on the frame.
    :param frame: frame in which to draw
    :param rect: list of [x, y, w, h]
    :color: color of rectangle
    :return: frame with rectangle
    """
    rect_frame = frame
    for x, y, w, h in rect:
        rect_frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
    return rect_frame


def draw_tracker_name(
    frame: frame,
    tracker_name: str,
    tracker_number: int = 1,
    color: tuple[int, int, int] = (0, 255, 0),
) -> frame:
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
