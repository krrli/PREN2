
from abc import ABC
from abc import abstractmethod

class Camera(ABC):

    def __init__(self, camspec = None):
        self._camspec = camspec
        self._camera = self.create_camera(camspec)


    @abstractmethod
    def capture(self):
        pass

    @abstractmethod
    def create_camera(self, camspec = None):
        pass

    @abstractmethod
    def free_camera(self):
        pass