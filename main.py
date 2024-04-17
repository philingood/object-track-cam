import logging
import time
from typing import Tuple

from cv2 import (
    CascadeClassifier,
    VideoCapture,
    destroyAllWindows,
    destroyWindow,
    imshow,
    selectROI,
)
from cv2.legacy import TrackerCSRT

import config
from modules.frame import (
    get_gray_frame,
    resize_frame,
)
from modules.keys import Keys
from modules.tracker import Tracker, detect_face

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
)


def get_frame(cap: VideoCapture) -> Tuple:
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.
    :param cap: cv2.VideoCapture
    :return: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = resize_frame(frame, scale=0.8)
    return (frame, get_gray_frame(frame))


if __name__ == "__main__":
    key = Keys()

    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = VideoCapture(1)
    time.sleep(1)

    # Trackers
    csrt = Tracker(
        TrackerCSRT.create(),
        "CSRT tracker",
        TrackerCSRT.create().update,
        tracker_number=1,
        color=(0, 0, 255),
    )
    face = Tracker(
        CascadeClassifier("data/haarcascade_frontalface_default.xml"),
        "Face tracker",
        detect_face,
        tracker_number=2,
        color=(255, 0, 0),
    )

    # Main loop
    while True:
        frame, gray = get_frame(cap)
        face.process(frame, "F", gray, face.tracker)
        csrt.process(frame, "S", gray)

        imshow("Tracker", frame)

        # Control
        if key.isPressed("f"):
            face.start_tracking()
        if key.isPressed("s"):
            object = selectROI(gray)
            destroyWindow("ROI selector")
            csrt.tracker.init(gray, object)
            csrt.start_tracking()

        # Press t key to start centering
        if key.isPressed("t"):
            # TODO: Add more tracker types
            face.start_centering()

        # Press Q key to stop all trackers
        if key.isPressed("Q"):
            csrt.stop_tracking()
            face.stop_tracking()

        # Press Esc key to stop program
        if key.escIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
