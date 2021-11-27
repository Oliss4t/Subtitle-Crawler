from abc import ABCMeta, abstractmethod


class MediaMetaScraper(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def get_movie_info_by_id(self):
        pass

    @abstractmethod
    def get_series_info_by_id(self):
        pass

    @abstractmethod
    def get_season_info_by_id(self):
        pass

    @abstractmethod
    def get_episode_info_by_id(self):
        pass
