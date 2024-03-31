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
    # Make a tracker and turn on the camera
    tracker = cv2.TrackerCSRT_create()
    # NOTE: Select number of your camera 0 or 1 or 2 …
    cap = cv2.VideoCapture(2)
    time.sleep(1)

    # Get the first frame and select the object
    # and initialize the tracker
    frame, gray = get_frame(cap)
    object = cv2.selectROI(gray)
    tracker.init(gray, object)

    print("Start tracking!")
    print("Press Esc to exit\n")

    # Variables for backuping
    bf_cout = 0

    # Main loop
    while True:
        # Get the frame and update the tracker
        frame, gray = get_frame(cap)
        success, box = tracker.update(gray)

        # print("Frame: ", bf_cout)

        # If the object is tracked on the frame, draw a rectangle
        if success:
            m.draw_rect(frame, box=box)

        # Count the frames
        bf_cout += 1

        # Show the frame
        cv2.imshow("FRAME", frame)

        # Wait for s key to reselect the object
        if cv2.waitKey(1) & 0xFF == ord("s"):
            object = cv2.selectROI(gray)
            tracker.init(gray, object)
            continue

        # Wait for Esc key to stop
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Stop the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
