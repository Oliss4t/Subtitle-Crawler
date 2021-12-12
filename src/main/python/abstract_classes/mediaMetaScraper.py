from abc import ABCMeta, abstractmethod


class MediaMetaScraper(metaclass=ABCMeta):
    """
    This is an abstract class defining a media crawler and the methods to implement.
    The implementing class should scrape additional information about the movie as well as the movie image
    and save them on the file path.
    """
    def __init__(self):
        pass

    @abstractmethod
    def download_movie_info_by_ids(self):
        pass

    @abstractmethod
    def save_movie_infos_in_directory(self):
        pass

    @abstractmethod
    def save_movie_image_in_directory(self):
        pass

    @abstractmethod
    def get_series_info_by_id(self):
        pass
