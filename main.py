import cv2
import time


tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture(0)
time.sleep(1)
ret, frame = cap.read()
frame = cv2.resize(frame, (1280, 720))
# object = cv2.selectROI(frame)
# tracker.init(frame, object)

object_selected = False
object_roi = None


def mouse_click(event, x, y, flags, param):
    global object_selected, object_roi
    if event == cv2.EVENT_LBUTTONDOWN:
        object_roi = (x, y, 1, 1)
        object_selected = True


cv2.namedWindow("FRAME")
cv2.setMouseCallback("FRAME", mouse_click)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if object_selected:
        tracker.init(frame, object_roi)
        object_selected = False

    frame = cv2.resize(frame, (1280, 720))
    success, box = tracker.update(frame)
    if success:
        (x, y, w, h) = [int(a) for a in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        # cv2.line(frame, (cx, 0), (cx, 480), (0, 0, 255), 2)

    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
