"""
Module containing the Tracker class
"""

try:
    from draw import draw_point, draw_rect, draw_region, draw_text, draw_tracker_name
    from frame import (
        central_region,
        define_region,
        divide_frame_into_regions,
    )
    from keys import Keys
    from servomotor import Servomotor
except ImportError:
    from .draw import draw_point, draw_rect, draw_region, draw_text, draw_tracker_name
    from .frame import (
        central_region,
        define_region,
        divide_frame_into_regions,
    )
    from .keys import Keys
    from .servomotor import Servomotor
import logging
from typing import Sequence, Tuple

import numpy as np
from config import INITIAL_X, INITIAL_Y
from cv2 import CascadeClassifier, selectROI
from cv2.legacy import TrackerCSRT
from cv2.typing import Rect


logging.getLogger("__name__")


key = Keys()
servoX = Servomotor("X")
servoY = Servomotor("Y", correction=0.75)


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
        self.angleX = INITIAL_X
        self.angleY = INITIAL_Y
        self.total_frames_count = 0
        self.success_frames_count = 0
        self.success_tracked_count = 0

    def process(self, frame: np.ndarray, STOP_KEY: str, *args) -> None:
        if self.track:
            self.total_frames_count += 1
            draw_tracker_name(
                frame,
                f"{self.tracker_number} {self.name}",
                self.tracker_number,
                color=self.color,
            )
            success, rect = self.func(*args)
            if success:
                self.success_frames_count += 1
                try:
                    frame = draw_rect(frame, rect, self.color)
                    logging.debug(
                        f"success: {success}, rect: {rect}, type: {type(rect)}"
                    )
                except Exception as e:
                    logging.debug(e)
                    logging.debug(
                        f"success: {success}, rect: {rect}, type: {type(rect)}"
                    )

            if self.centering:
                self.folow_center(frame, success, rect)

        if key.isPressed(STOP_KEY):
            self.stop_tracking()

    def calculate_coordinates(
        self,
        position: Tuple[int, int, int],
        central_region: np.ndarray,
        center_of_frame: Tuple[int, int],
    ) -> Tuple[int, int]:
        """
        Calculates abstract coordinates for servo motor.
        In essence, the coordinate center is transferred to the center of
        the frame and the region index is recalculated.
        :param position: tuple(i, j, n), where i, j - index of the region
        in which center of the object is located, n - quontity of regions
        by width.
        :param central_region: coordinates of rectangle of the central region.
        :param center: tuple(x, y), where x, y - coordinates of the center of
        the object.
        :return: tuple(vx, vy)
        """
        x, y = center_of_frame
        i, j, n = position
        xcr, ycr, wcr, hcr = [a for a in central_region[0]]
        half = n // 2
        vx: int
        vy: int

        # If center of the object is in the central region
        if x in range(xcr, xcr + wcr) and y in range(ycr, ycr + hcr):
            vx = vy = 0
            return (vx, vy)

        # If center of the object is in the left half of the frame
        if i <= half:
            vx = i - (half + 1)
        # If center of the object is in the right half of the frame
        else:
            vx = i - half

        # If the center of the object is in the top half of the frame
        if j <= half:
            vy = -j + (half + 1)
        # If the center of the object is in the bottom half of the frame
        else:
            vy = -j + half
        return (vx, vy)

    def get_box_center(self, rect: Sequence[Rect]) -> Tuple[int, int]:
        """
        Gets the center of the rectangle.
        :return: Tuple of (x, y)
        """
        x, y, w, h = rect[0][0], rect[0][1], rect[0][2], rect[0][3]
        cx: int = x + w // 2
        cy: int = y + h // 2
        return (cx, cy)

    def folow_center(self, frame: np.ndarray, success: bool, rect) -> None:
        # Define central region in which coordinates is zero
        central_region_rect = central_region(frame)
        WHITE = (255, 255, 255)
        draw_rect(frame, central_region_rect, color=WHITE)

        if success:
            # Center of object
            center = self.get_box_center(rect)
            draw_point(frame, center)

            # Divide frame into regions and draw a region in which
            # center is
            regions = divide_frame_into_regions(frame, n=20)
            region_with_center = define_region(center, regions)
            draw_region(frame, region_with_center, regions)

            # Get angles of servomotors
            coordinates = self.calculate_coordinates(
                region_with_center, central_region(frame), center
            )
            if coordinates == (0, 0):
                self.success_tracked_count += 1

            draw_text(frame, f"{coordinates}", position=center)
            logging.debug(coordinates)
            self.angleX = servoX.calculate_angle(coordinates[0], self.angleX)
            self.angleY = servoY.calculate_angle(coordinates[1], self.angleY)
            logging.debug((self.angleX, self.angleY))

            # Send angles to servomotors
            servoX.send_data(self.angleX)
            servoY.send_data(self.angleY)

    def get_efficiency(self):
        print("\n")
        print(f"Tracker {self.name}:")
        s = self.success_frames_count
        st = self.success_tracked_count
        t = self.total_frames_count
        print(f"Total number of frames: {t}")
        print(f"Number of successful frames: {s}")
        print(f"Number of frames when object was in the center: {st}")

        if t > 0:
            print(f"Efficiency: {s / t * 100:.2f}%")
            print(f"Total efficiency: {st / t * 100:.2f}%")
        else:
            print("Efficiency is not available. No frames were processed")

    def start_tracking(self):
        self.track = True

    def stop_tracking(self):
        self.track = False

    def start_centering(self):
        self.centering = True

    def stop_centering(self):
        self.centering = False


class CSRTracker(Tracker):
    def init(self, frame):
        self.tracker = self.tracker.create()
        obj = selectROI(frame)
        self.tracker.init(frame, obj)
        self.func = self.tracker.update


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


csrt = CSRTracker(
    TrackerCSRT,
    "CSRT tracker",
    # TrackerCSRT.create().update,
    ...,
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


if __name__ == "__main__":
    from cv2 import (
        VideoCapture,
        destroyAllWindows,
        imshow,
    )

    from frame import get_frame

    logging.basicConfig(level=logging.DEBUG)

    cap = VideoCapture(0)

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
