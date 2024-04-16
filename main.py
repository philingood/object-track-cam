import time
import numpy as np
from typing import Tuple, Sequence
from cv2 import typing
import logging

from cv2.legacy import TrackerCSRT
from cv2 import (
    CascadeClassifier,
    VideoCapture,
    selectROI,
    imshow,
    destroyAllWindows,
)
import modules.methods as m
from modules.draw import (
    draw_text,
    draw_point,
    draw_region,
)
from modules.frame import resize_frame, get_gray_frame
from modules.keys import Keys
from modules.tracker import Tracker


def get_frame(cap: VideoCapture) -> Tuple:
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.

    Returns: Tuple of the frame and its gray version.
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
    logging.basicConfig(level=logging.DEBUG)

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
            csrt.tracker.init(gray, object)
            csrt.start_tracking()

        # # Press s key to start or reselect the object for CSRT tracker
        # if keys.keyIsPressed("s"):
        #     object = cv2.selectROI(gray)
        #     tracker.init(gray, object)
        #     CSRT = True

        # if FACE:
        #     success, face = m.detect_face(gray, faces)
        #     if CSRT:
        #         tracker_number = 2
        #     if TRACK_FACE and success:
        #         show_center(frame, face)
        #     draw_tracker_name(
        #         frame,
        #         f"{tracker_number} FACE tracker",
        #         tracker_number,
        #         color=FACE_COLOR,
        #     )
        #     draw_rect(frame, rect=face, color=FACE_COLOR)
        #     if keys.keyIsPressed("F"):
        #         FACE = False
        #         TRACK_FACE = False

        # Count the frames
        # bf_cout += 1
        # print("Frame: ", bf_cout)

        # Press Q key to stop all trackers
        if key.isPressed("Q"):
            csrt.stop_tracking()
            face.stop_tracking()

        # # Press 1 or 2 to focus camera on the object
        # if keys.keyIsPressed("1"):
        #     if tracker_number == 2 or CSRT:
        #         TRACK_CSRT = True
        #     elif FACE:
        #         TRACK_FACE = True
        # elif keys.keyIsPressed("2"):
        #     if FACE:
        #         TRACK_FACE = True

        # Press Esc key to stop
        if key.escKeyIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
