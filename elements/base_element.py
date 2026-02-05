from abc import ABC, abstractmethod


class BaseElement(ABC):
    def __init__(self, name, description, img=None):
        self.name = name
        self.description = description
        self.img = img

    @abstractmethod
    def apply(self, player):
        pass
