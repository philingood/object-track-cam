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
    cap = cv2.VideoCapture(2)
    time.sleep(1)

    # Get the first frame and select the object
    # and initialize the tracker
    frame, gray = get_frame(cap)
    object = cv2.selectROI(gray)
    print(object)
    tracker.init(gray, object)

    print("\nStart tracking!\n")
    print("Press Esc to exit\n")

    # Variables for backuping
    bf_cout = 0
    gray_backup = [None, None, None, None]
    success_backup = False

    # Main loop
    while True:
        # Get the frame and update the tracker
        frame, gray = get_frame(cap)
        success, box = tracker.update(gray)

        # print("Frame: ", bf_cout)

        # Get backup frames
        if success_backup:
            if bf_cout % 5 == 0:
                gray_backup[0] = gray
            if bf_cout % 20 == 0:
                gray_backup[1] = gray
            if bf_cout % 55 == 0:
                gray_backup[2] = gray
            if bf_cout % 101 == 0:
                gray_backup[3] = gray

        # If the object is tracked on the frame, draw a rectangle
        if success:
            m.draw_rect(frame, box=box)
            success_backup = True
            if bf_cout % 56 == 0 and bf_cout > 0:
                # print("Frame: ", bf_cout)
                success, box = tracker.update(gray_backup[2])
                if success:
                    print("Backup 55: ", bf_cout)
                    m.draw_rect(frame, box=box)
                    cv2.imshow("BACKUP 55", frame)
            if bf_cout % 102 == 0 and bf_cout > 0:
                success, box = tracker.update(gray_backup[3])
                if success:
                    print("Backup 101: ", bf_cout)
                    m.draw_rect(frame, box=box)
                    cv2.imshow("BACKUP 101", frame)
        # If the object is not tracked, use backup frame
        elif bf_cout > 0:
            success, box = tracker.update(gray_backup[1])
            if success:
                m.draw_rect(frame, box=box)
                success_backup = True
        else:
            success_backup = False

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
