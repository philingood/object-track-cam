import cv2

frame = cv2.UMat
rectangle = cv2.typing.Rect


# ~~~~~~~~~~ Detectors ~~~~~~~~~~
def detect_face(frame: frame, faces) -> rectangle:
    return faces.detectMultiScale(frame, scaleFactor=2.1, minNeighbors=2)


# ~~~~~~~~~~ Frame processing ~~~~~~~~~~
def resize_frame(frame: frame, scale=0.5) -> frame:
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def get_gray_frame(frame: frame) -> frame:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# ~~~~~~~~~~ Drawings ~~~~~~~~~~~
def draw_rect(
    frame: frame, rect: rectangle, color: tuple[int, int, int] = (0, 255, 0)
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
