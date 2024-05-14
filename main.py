import logging
import time

from cv2 import (
    VideoCapture,
    destroyAllWindows,
    imshow,
)

import config
from modules.frame import get_frame
from modules.keys import Keys
from modules.tracker import csrt, face

args = config.parse_arguments()

logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
)


if __name__ == "__main__":
    key = Keys()

    cap = VideoCapture(config.CAM)
    time.sleep(1)

    while True:
        frame, gray = get_frame(cap)
        face.process(frame, "F", gray, face.tracker)
        csrt.process(frame, "S", gray)

        imshow("Tracker", frame)

        # ~~~~~~~~~~~~ Control ~~~~~~~~~~~~
        if key.isPressed("f"):
            face.start_tracking()
            csrt.stop_tracking()
        if key.isPressed("s"):
            csrt.init(frame)
            csrt.start_tracking()
            face.stop_tracking()

        # Press c/C key to start/stop centering
        if key.isPressed("c"):
            # TODO: Add more tracker types (mb Yolo)
            if face.track:
                face.start_centering()
            if csrt.track:
                csrt.start_centering()
        if key.isPressed("C"):
            face.stop_centering()
            csrt.stop_centering()

        # Press Q key to stop all trackers
        if key.isPressed("Q"):
            csrt.stop_tracking()
            face.stop_tracking()

        # Press Esc key to stop program
        if key.escIsPressed():
            break
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Metrics
    face.get_efficiency()
    csrt.get_efficiency()

    # Stop the camera and close all windows
    cap.release()
    destroyAllWindows()
