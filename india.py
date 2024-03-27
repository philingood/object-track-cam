import cv2
import time


def track(img):
    """
    Функция для получения координат объекта из трекера

    Параметры:
    - img: Изображение на котором определяется объект
    """
    success, box = tracker.update(img)
    if success:
        # Получаем координаты объекта на изображении
        (x, y, w, h) = [int(a) for a in box]

        # Построение всяких квадратов синих и проч. для визуального контроля
        # отслеживания объекта
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
        cv2.line(img, (cx, 0), (cx, 480), (0, 0, 255), 2)
        a = int(cx) // 65

        print(a)


if __name__ == "__main__":
    # Включение камеры и задание размера кадра
    cap = cv2.VideoCapture(2)
    time.sleep(1)
    ret, frame = cap.read()

    # Захват объекта на первом кадре видеопотока
    frame = cv2.resize(frame, (frame.shape[1] // 3, frame.shape[0] // 3))
    object = cv2.selectROI(frame)

    # Включение отслеживания объекта в видеопотоке
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, object)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1] // 3, frame.shape[0] // 3))

        track(frame)

        cv2.imshow("FRAME", frame)

        # По нажатию ESC программа завершается
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Завершение программы и закрытие всех окон
    cap.release()
    cv2.destroyAllWindows()
