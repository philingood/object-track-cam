"""
Module containing the Tracker class
"""

import logging
from typing import Tuple, Sequence
from cv2.typing import Rect

import numpy as np
from cv2 import error as cv2error
from cv2 import CascadeClassifier

logging.getLogger("__name__")


try:
    from draw import draw_rect, draw_tracker_name, draw_region, draw_point, draw_text
    from frame import (
        divide_frame_into_regions,
        define_region,
        get_gray_frame,
        resize_frame,
        central_region,
    )
    from servomotor import Servomotor
    from keys import Keys
except ImportError:
    from .draw import draw_rect, draw_tracker_name, draw_region, draw_point, draw_text
    from .frame import (
        divide_frame_into_regions,
        define_region,
        get_gray_frame,
        resize_frame,
        central_region,
    )
    from .servomotor import Servomotor
    from .keys import Keys

key = Keys()


class Tracker:
    def __init__(
        self,
        tracker,
        name: str,
        main_function,
        tracker_number: int = 1,
        track: bool = False,
        centering: bool = False,
        color: Tuple = (255, 0, 0),
    ):
        self.tracker = tracker
        self.name = name
        self.tracker_number = tracker_number
        self.track = track
        self.centering = centering
        self.color = color
        self.func = main_function

    def process(self, frame: np.ndarray, STOP_KEY: str, *args) -> None:
        if self.track:
            draw_tracker_name(
                frame,
                f"{self.tracker_number} {self.name}",
                self.tracker_number,
                color=self.color,
            )
            success, rect = self.func(*args)
            if success:
                try:
                    draw_rect(frame, rect, self.color)
                except (TypeError, ValueError, cv2error) as e:
                    logging.error(e)
                if self.centering:
                    # Center of object
                    center = self.get_box_center(rect)
                    draw_point(frame, center)

                    # Define central region in which velocity is zero
                    central_region_rect = central_region(frame)
                    draw_rect(frame, central_region_rect,
                              color=(255, 255, 255))

                    # Divide frame into regions and draw a region in which
                    # center is
                    regions = divide_frame_into_regions(frame)
                    region_with_center = define_region(center, regions)
                    draw_region(frame, region_with_center, regions)

                    # Get velocity of servomotor
                    velocity = Servomotor.calculate_velocity(
                        region_with_center, central_region(frame), center
                    )
                    draw_text(frame, f"{velocity}", position=center)
            else:
                logging.debug(f"{success}, {rect}")

        if key.isPressed(STOP_KEY):
            self.stop_tracking()

    def get_box_center(self, rect: Sequence[Rect]) -> Tuple[int, int]:
        """
        Gets the center of the rectangle.
        :return: Tuple of (x, y)
        """
        x, y, w, h = rect[0][0], rect[0][1], rect[0][2], rect[0][3]
        cx: int = x + w // 2
        cy: int = y + h // 2
        return (cx, cy)

    def start_tracking(self):
        self.track = True

    def stop_tracking(self):
        self.track = False

    def start_centering(self):
        self.centering = True

    def stop_centering(self):
        self.centering = False


def detect_face(
    frame: np.ndarray, faces: CascadeClassifier
) -> Tuple[bool, Sequence[Rect]]:
    """
    Detects faces in the frame.
    :param frame: frame in which to detect
    :param faces: pre-trained classifier of faces
    :return: tuple(bool, List)
    """
    # https://stackoverflow.com/questions/36218385/parameters-of-detectmultiscale-in-opencv-using-python
    face = faces.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=3)
    success = True
    if len(face) == 0:
        success = False
    return (success, face)


if __name__ == "__main__":
    from cv2.legacy import TrackerCSRT
    from cv2 import (
        CascadeClassifier,
        VideoCapture,
        destroyAllWindows,
        imshow,
    )

    logging.basicConfig(level=logging.DEBUG)

    def get_frame(cap: VideoCapture) -> Tuple:
        """Get a frame from the camera and resize it.
        You can add more methods here if you want.
        Returns: Tuple of the frame and its gray version.
        """
        frame = cap.read()[1]
        frame = resize_frame(frame, scale=0.5)
        return (frame, get_gray_frame(frame))

    cap = VideoCapture(0)

    csrt = Tracker(
        TrackerCSRT.create(),
        "CSRT tracker",
        TrackerCSRT.create().update,
        tracker_number=1,
        color=(0, 0, 255),
    )
    face = Tracker(
        CascadeClassifier("../data/haarcascade_frontalface_default.xml"),
        "Face tracker",
        detect_face,
        tracker_number=2,
        color=(255, 0, 0),
    )

    while True:
        frame, gray = get_frame(cap)
        face.process(frame, "F", gray, face.tracker)
        csrt.process(frame, "S", gray)

        imshow("Tracker", frame)

        if key.isPressed("f"):
            face.start_tracking()
        if key.isPressed("s"):
            csrt.start_tracking()

        if key.escIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
