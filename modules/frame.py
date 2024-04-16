"""
Frame processing module
"""

import cv2
import numpy as np
from typing import Tuple


def get_frame_size(frame: np.ndarray) -> Tuple[int, int]:
    return (frame.shape[1], frame.shape[0])


def resize_frame(frame: np.ndarray, scale: float = 0.5) -> np.ndarray:
    w = int(frame.shape[1] * scale)
    h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def get_gray_frame(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
