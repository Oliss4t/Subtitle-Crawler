from abc import ABCMeta, abstractmethod


class Media(metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def year(self):
        pass

    @property
    @abstractmethod
    def image(self):
        pass

    @property
    @abstractmethod
    def genres(self):
        pass

    @property
    @abstractmethod
    def runtimes(self):
        pass

    @property
    @abstractmethod
    def votes(self):
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def export_to_file(self):
        pass

