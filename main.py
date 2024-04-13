import cv2
import time
import methods as m


def get_frame(cap):
    """Get a frame from the camera and resize it.
    You can add more methods here if you want.

    Returns: Tuple of the frame and its gray version.
    """
    frame = cap.read()[1]
    frame = m.resize_frame(frame, scale=0.3)
    return (frame, m.get_gray_frame(frame))


if __name__ == "__main__":
    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = cv2.VideoCapture(2)
    time.sleep(1)

    # Tracker
    tracker = cv2.TrackerCSRT_create()
    TRACK = False

    # Auto trackers
    # Face
    faces = cv2.CascadeClassifier(
        "training/haarcascade_frontalface_default.xml")
    FACE = False

    bf_cout = 0

    # Main loop
    while True:
        frame, gray = get_frame(cap)

        tracker_number = 1
        if TRACK:
            # Update the tracker
            success, box = tracker.update(gray)
            m.draw_tracker_name(frame, "CSRT tracker")

            # If the object is tracked on the frame, draw a rectangle
            if success:
                m.draw_rect(frame, box=box)

        if FACE:
            if TRACK:
                tracker_number = 2
            m.draw_tracker_name(frame, "FACE tracker", tracker_number)
            m.draw_rect(frame, rect=m.detect_face(gray, faces))

        # Count the frames
        bf_cout += 1
        # print("Frame: ", bf_cout)

        # Show the frame
        cv2.imshow("FRAME", frame)

        # Wait for f key to start face tracking
        if cv2.waitKey(1) & 0xFF == ord("f"):
            FACE = True
            continue
        # Wait for F key to stop face tracking
        if cv2.waitKey(1) & 0xFF == ord("F"):
            FACE = False
            continue

        # Wait for s key to reselect the object for Tracker
        if cv2.waitKey(1) & 0xFF == ord("s"):
            object = cv2.selectROI(gray)
            tracker.init(gray, object)
            TRACK = True
            continue
        # Wait for S key to stop CSRT Tracker
        if cv2.waitKey(1) & 0xFF == ord("S"):
            TRACK = False
            continue

        # Wait for Q key to stop all trackers
        if cv2.waitKey(1) & 0xFF == ord("Q"):
            if TRACK:
                TRACK = False
            if FACE:
                FACE = False
            continue

        # Wait for Esc key to stop
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Stop the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
