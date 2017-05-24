from threading import Thread
from threading import Lock
from threading import Event
from queue import Queue
from queue import Empty


class QueueWorker:

    def __init__(self, romanNumeralDetector):
        self.number_detected = 0
        self.idle = False
        self._romanNumeralDetector = romanNumeralDetector
        self._queues_lock = Lock()
        self._frame_buffers = []
        self._stop_working_event = Event()

    def add_frame_buffer(self, queue):
        with self._queues_lock:
            self._frame_buffers.append(queue)

    def start_working(self):
        thread = Thread(args=(), target=self._work_on_queues)
        thread.start()

    def _work_on_queues(self):
        while not self._stop_working_event.is_set():
            with self._queues_lock:
                did_work = False
                for frame_buffer in self._frame_buffers:
                    try:
                        frame = frame_buffer.frame_queue.get_nowait()
                        number_result = self._romanNumeralDetector.capture(frame)
                        if number_result != 0:
                            print("QUEE: Numer detected " + str(number_result))
                            self.numberDetected = number_result
                        did_work = True
                    except Empty:
                        pass

                self.idle = not did_work

    def stop_capturing(self):
        self._stop_working_event.set()