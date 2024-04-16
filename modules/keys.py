import cv2


class Keys:
    def __init__(self):
        pass

    def escKeyIsPressed(self):
        if cv2.waitKey(1) & 0xFF == 27:
            return True
        else:
            return False

    def waitKeyIf(self, key: str) -> bool:
        if cv2.waitKey(1) & 0xFF == ord(key):
            return True
        else:
            return False

    def isPressed(self, key: str) -> bool:
        return self.waitKeyIf(key)
