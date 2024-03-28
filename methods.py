import cv2
import numpy as np


def resize_frame(frame, scale=0.5):
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def redraw_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.Canny(frame, 100, 140)
    con = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    redrawn_frame = np.zeros(frame.shape, np.uint8)
    return cv2.drawContours(redrawn_frame, con, -1, (230, 111, 148), 1)


def get_gray_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def detect_face(frame, faces):
    return faces.detectMultiScale(frame, scaleFactor=2.1, minNeighbors=2)


def draw_rect(frame, rect=None, box=None):
    """Draw rectangle on the frame.
    Args:
        rect: list of [x, y, w, h]
        box: Tuple of (x, y, w, h)
    """
    rect_frame = frame
    if rect:
        for x, y, w, h in rect:
            rect_frame = cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    elif box:
        (x, y, w, h) = box
        rect_frame = cv2.rectangle(
            frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    return rect_frame


def mouse_click(event, x, y, flags, param):
    # TODO: refactor. This do not work by now
    global object_selected, object_roi
    if event == cv2.EVENT_LBUTTONDOWN:
        object_roi = (x, y, 1, 1)
        object_selected = True
