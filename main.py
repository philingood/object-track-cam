import cv2
import time
import methods as m
from keys import Keys


def get_frame(cap) -> tuple:
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.

    Returns: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = m.resize_frame(frame, scale=0.3)
    return (frame, m.get_gray_frame(frame))


def show_center(frame, rect) -> None:
    """Show the center of the rectangle."""
    center = m.get_box_center(rect)
    print(f"Center coordinates: {center}")
    m.draw_point(frame, center)


if __name__ == "__main__":
    keys = Keys()

    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = cv2.VideoCapture(2)
    time.sleep(1)

    # Tracker
    tracker = cv2.TrackerCSRT_create()
    CSRT_COLOR = (0, 0, 255)
    CSRT = False
    TRACK_CSRT = False

    # Face tracker
    faces = cv2.CascadeClassifier(
        "training/haarcascade_frontalface_default.xml")
    FACE_COLOR = (255, 0, 0)
    FACE = False
    TRACK_FACE = False

    bf_cout = 0

    # Main loop
    while True:
        tracker_number = 1
        frame, gray = get_frame(cap)

        if CSRT:
            success, box = tracker.update(gray)
            m.draw_tracker_name(
                frame, f"{tracker_number} CSRT tracker", color=CSRT_COLOR
            )
            if success:
                m.draw_rect(frame, rect=[box], color=CSRT_COLOR)
            if keys.keyIsPressed("S"):
                CSRT = False

        if FACE:
            success, face = m.detect_face(gray, faces)
            if CSRT:
                tracker_number = 2
            if TRACK_FACE and success:
                show_center(frame, face)
            m.draw_tracker_name(
                frame,
                f"{tracker_number} FACE tracker",
                tracker_number,
                color=FACE_COLOR,
            )
            m.draw_rect(frame, rect=face, color=FACE_COLOR)
            if keys.keyIsPressed("F"):
                FACE = False
                TRACK_FACE = False

        # Count the frames
        # bf_cout += 1
        # print("Frame: ", bf_cout)

        # Show the frame
        cv2.imshow("FRAME", frame)

        # Press f key to start face tracking
        if cv2.waitKey(1) & 0xFF == ord("f"):
            FACE = True

        # Press s key to start or reselect the object for CSRT tracker
        if keys.keyIsPressed("s"):
            object = cv2.selectROI(gray)
            tracker.init(gray, object)
            CSRT = True

        # Press Q key to stop all trackers
        if keys.keyIsPressed("Q"):
            if CSRT:
                CSRT = False
            if FACE:
                FACE = False

        # Press 1 or 2 to focus camera on the object
        if keys.keyIsPressed("1"):
            if tracker_number == 2 or CSRT:
                TRACK_CSRT = True
            else:
                TRACK_FACE = True
        elif keys.keyIsPressed("2"):
            if FACE:
                TRACK_FACE = True

        # Press Esc key to stop
        if keys.escKeyIsPressed():
            break

    # Stop the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
