from threading import Thread


class QueueWorker:
    def __init__(self):
        self.thread = Thread(args=(), target=self._hoi())
        self.numberDetected = 0

        # TODO: Liste von Queues zum abarbeiten!


    def _hoi(self):
        print("hoi")