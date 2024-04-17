import cv2


class Keys:
    def __init__(self):
        pass

    def waitKeyIf(self, key: str) -> bool:
        return cv2.waitKey(1) & 0xFF == ord(key)

    def escIsPressed(self):
        ESC = "\x1b"
        return self.waitKeyIf(ESC)

    def isPressed(self, key: str) -> bool:
        return self.waitKeyIf(key)
