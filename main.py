import cv2
import time
import methods as m
from keys import Keys


def get_frame(cap):
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.

    Returns: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = m.resize_frame(frame, scale=0.3)
    return (frame, m.get_gray_frame(frame))


if __name__ == "__main__":
    keys = Keys()

    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = cv2.VideoCapture(2)
    time.sleep(1)

    # Tracker
    tracker = cv2.TrackerCSRT_create()
    TRACK_COLOR = (0, 0, 255)
    TRACK = False

    # Auto trackers
    # Face
    faces = cv2.CascadeClassifier(
        "training/haarcascade_frontalface_default.xml")
    FACE_COLOR = (255, 0, 0)
    FACE = False

    bf_cout = 0

    # Main loop
    while True:
        tracker_number = 1
        frame, gray = get_frame(cap)

        if TRACK:
            success, box = tracker.update(gray)
            m.draw_tracker_name(
                frame, f"{tracker_number} CSRT tracker", color=TRACK_COLOR
            )
            if success:
                m.draw_rect(frame, rect=[box], color=TRACK_COLOR)
            if keys.keyIsPressed("S"):
                TRACK = False

        if FACE:
            if TRACK:
                tracker_number = 2
            m.draw_tracker_name(
                frame,
                f"{tracker_number} FACE tracker",
                tracker_number,
                color=FACE_COLOR,
            )
            m.draw_rect(frame, rect=m.detect_face(
                gray, faces), color=FACE_COLOR)
            if keys.keyIsPressed("F"):
                FACE = False

        # Count the frames
        # bf_cout += 1
        # print("Frame: ", bf_cout)

        # Show the frame
        cv2.imshow("FRAME", frame)

        # Wait for f key to start face tracking
        if cv2.waitKey(1) & 0xFF == ord("f"):
            FACE = True

        # Wait for s key to start or reselect the object for CSRT tracker
        if keys.keyIsPressed("s"):
            object = cv2.selectROI(gray)
            tracker.init(gray, object)
            TRACK = True

        # Wait for Q key to stop all trackers
        if keys.keyIsPressed("Q"):
            if TRACK:
                TRACK = False
            if FACE:
                FACE = False

        # Wait for Esc key to stop
        if keys.escKeyIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
