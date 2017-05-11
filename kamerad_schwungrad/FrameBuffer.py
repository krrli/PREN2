from queue import Queue
from threading import Thread, Lock, Event

class FrameBuffer:
    '''
    chäri steht vor Ampel:
    Kamera rechts = Bubeluschka
    Kamera links = Kari
    '''
    BUBELUSCHKA = 0
    KARI = 1

    def __init__(self, BubeluschkaOrKari):
        self.frame_queue = Queue()
        self._camera_lock = Lock()
        self._camera = None
        self._capture_stop_event = Event()

        if(BubeluschkaOrKari.lower == "bubeluschka"):
            self.set_camera(FrameBuffer.BUBELUSCHKA)
        if (BubeluschkaOrKari.lower == "kari"):
            self.set_camera(FrameBuffer.KARI)


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
                frame = self._camera.capture()

            if not frame is None:
                self.frame_queue.put_nowait(frame)

    def stop_capturing(self):
        self._capture_stop_event.set()

