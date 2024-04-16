import logging
import time
from typing import Sequence, Tuple

import config
import modules.methods as m
import numpy as np
from cv2 import (
    CascadeClassifier,
    VideoCapture,
    destroyAllWindows,
    destroyWindow,
    imshow,
    selectROI,
    typing,
)
from cv2.legacy import TrackerCSRT
from modules.draw import (
    draw_point,
    draw_region,
    draw_text,
)
from modules.frame import get_gray_frame, resize_frame
from modules.keys import Keys
from modules.tracker import Tracker

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_frame(cap: VideoCapture) -> Tuple:
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.
    :param cap: cv2.VideoCapture
    :return: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = resize_frame(frame, scale=0.5)
    return (frame, get_gray_frame(frame))


def show_center(frame: np.ndarray, rect: Sequence[typing.Rect]) -> None:
    """Show the center of the rectangle."""
    center = m.get_box_center(rect)
    print(f"Center coordinates: {center}")
    draw_point(frame, center)
    regions = m.divide_frame_into_regions(frame)
    region_with_center = m.define_region(center, regions)
    velocity = m.calculate_velocity(region_with_center)
    draw_text(frame, f"{velocity}", position=center)
    draw_region(frame, region_with_center, regions)


if __name__ == "__main__":
    key = Keys()

    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = VideoCapture(0)
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
        m.detect_face,
        tracker_number=2,
        color=(255, 0, 0),
    )

    bf_cout = 0

    # Main loop
    while True:
        frame, gray = get_frame(cap)
        face.process(frame, "F", gray, face.tracker)
        csrt.process(frame, "S", gray)

        imshow("Tracker", frame)

        if key.isPressed("f"):
            face.start_tracking()
        if key.isPressed("s"):
            object = selectROI(gray)
            destroyWindow("ROI selector")
            csrt.tracker.init(gray, object)
            csrt.start_tracking()

        # Count the frames
        # bf_cout += 1
        # print("Frame: ", bf_cout)

        # Press Q key to stop all trackers
        if key.isPressed("Q"):
            csrt.stop_tracking()
            face.stop_tracking()

        # Press Esc key to stop
        if key.escIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
