
import cv2

ENABLE_DEBUG = False


def show_debug_frame(window_title, frame):
    if ENABLE_DEBUG:
        cv2.imshow(window_title, frame)


def wait_for_input():
    while cv2.waitKey() & 0xFF == 'q':
        pass
