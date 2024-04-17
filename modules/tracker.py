"""
Module containing the Tracker class
"""

import logging
from typing import Tuple

import numpy as np
from cv2 import (
    CascadeClassifier,
    VideoCapture,
    destroyAllWindows,
    imshow,
)
from cv2 import error as cv2error
from cv2.legacy import TrackerCSRT

logging.getLogger("__name__")


try:
    from draw import draw_rect, draw_tracker_name
    from keys import Keys
except ImportError:
    from .draw import draw_rect, draw_tracker_name
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
            success, obj = self.func(*args)
            if success:
                try:
                    draw_rect(frame, obj, self.color)
                except (TypeError, ValueError, cv2error) as e:
                    logging.error(e)
                if self.centering:
                    pass
            else:
                logging.debug(f"{success}, {obj}")

        if key.isPressed(STOP_KEY):
            self.stop_tracking()

    def start_tracking(self):
        self.track = True

    def stop_tracking(self):
        self.track = False

    def start_centering(self):
        self.centering = True

    def stop_centering(self):
        self.centering = False


if __name__ == "__main__":
    import methods as m

    logging.basicConfig(level=logging.DEBUG)

    def get_frame(cap: VideoCapture) -> Tuple:
        """Get a frame from the camera and resize it.
        You can add more methods here if you want.

        Returns: Tuple of the frame and its gray version.
        """
        frame = cap.read()[1]
        frame = m.resize_frame(frame, scale=0.5)
        return (frame, m.get_gray_frame(frame))

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
        m.detect_face,
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

        if key.escKeyIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
