from queue import Queue
from threading import Thread, Lock, Event

class FrameBuffer:
    def __init__(self):
        self.frame_queue = Queue()
        self._camera_lock = Lock()
        self._camera = None
        self._capture_stop_event = Event()

    def set_camera(self, camera):
        with self._camera_lock:
            self._camera = camera

    def start_capturing(self):
        thread = Thread(args=(), target=self._capture)
        thread.start()


    def _capture(self):
        while not self._capture_stop_event.is_set():
            frame = None
            with self._camera_lock:
                ret, frame = self._camera.read()

            if not frame is None:
                self.frame_queue.put_nowait(frame)

    def stop_capturing(self):
        self._capture_stop_event.set()

