from queue import Queue
from threading import Thread, Lock, Event

class FrameBuffer:

    def __init__(self):
        self.frame_queue = Queue()
        self._camera_lock = Lock()
        self._camera = None
        self._capture_stop_event = Event()
        self._running = False


    def set_camera(self, camera):
        with self._camera_lock:
            self._camera = camera


    def start_capturing(self):
        if not self._running:
            self._running = True
            thread = Thread(args=(), target=self._capture)
            thread.start()

    def _capture(self):
        print("FBUF: starting")
        while not self._capture_stop_event.is_set():
            frame = None
            with self._camera_lock:
                if not self._camera is None:
                    ret, frame = self._camera.read()

            if not frame is None:
                print("FBUF: got frame")
                self.frame_queue.put_nowait(frame)
        print("FBUF: stopping")

    def stop_capturing(self):
        if self._running:
            self._capture_stop_event.set()

