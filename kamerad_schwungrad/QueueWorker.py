from threading import Thread
from threading import Lock
from threading import Event
from queue import Queue
from queue import Empty
import cv2


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
        framenum = [0, 0]
        print("QUEE: starting to work on queues")
        while not self._stop_working_event.is_set():
            with self._queues_lock:
                did_work = False
                fbnum = 0
                for frame_buffer in self._frame_buffers:
                    try:
                        frame = frame_buffer.frame_queue.get_nowait()
                        framenum[fbnum] = framenum[fbnum] + 1
                        filepath = "/tmp/pictures/" + str(fbnum) + "-" + str(framenum[fbnum]) + ".png"
                        print("QUEE: saving pictuture to " + filepath)
                        cv2.imwrite(filepath, frame) 
                        number_result = self._romanNumeralDetector.capture(frame)
                        if number_result != 0 and (not number_result is None):
                            print("QUEE: Numer detected " + str(number_result))
                            self.number_detected = number_result
                        did_work = True
                    except Empty:
                        pass
                    fbnum = fbnum + 1
                self.idle = not did_work
        print("QUEE: stopping")

    def stop_capturing(self):
        self._stop_working_event.set()
