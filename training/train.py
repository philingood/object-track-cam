import cv2
import methods as m


if __name__ == "__main__":
    faces = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
        # frame = m.resize_frame(frame, scale=0.3)
        # frame = m.redraw_frame(frame)
        m.draw_rect(frame, m.detect_face(m.get_gray_frame(frame), faces))

        cv2.imshow("FRAME", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
