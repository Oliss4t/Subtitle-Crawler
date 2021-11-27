from abc import ABCMeta, abstractmethod


class SubtitleScraper(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def check_server_status(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def download_movie_subtitle_by_id(self):
        pass

    @abstractmethod
    def download_series_subtitle_by_id(self):
        pass

    @abstractmethod
    def download_season_info_by_id(self):
        pass

    @abstractmethod
    def download_episode_info_by_id(self):
        pass