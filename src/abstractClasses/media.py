from abc import ABCMeta, abstractmethod


class Media(metaclass=ABCMeta):
    def __init__(self):
        pass

    # @classmethod
    # def __init_subclass__(cls):
    #     required_class_variables = [
    #         "name",
    #         "id",
    #         "year",
    #         "image",
    #         "genres",
    #         "runtimes",
    #         "rating",
    #         "plot",
    #     ]
    #     for var in required_class_variables:
    #         if not hasattr(cls, var):
    #             raise NotImplementedError(
    #                 f'Class {cls} lacks required `{var}` class attribute'
    #             )
    # @property
    # @abstractmethod
    # def name(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def id(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def year(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def image(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def genres(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def runtimes(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def rating(self):
    #     pass
    #
    # @abstractmethod
    # def plot(self):
    #     pass

    # @abstractmethod
    # def export_to_file(self):
    #     pass


