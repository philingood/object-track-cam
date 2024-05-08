from cv2 import waitKey


class Keys:
    def __init__(self):
        pass

    def waitKeyIf(self, key: str) -> bool:
        return waitKey(5) & 0xFF == ord(key)

    def escIsPressed(self):
        ESC = "\x1b"
        return self.waitKeyIf(ESC)

    def isPressed(self, key: str) -> bool:
        return self.waitKeyIf(key)
