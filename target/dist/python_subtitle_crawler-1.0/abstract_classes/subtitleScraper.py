from abc import ABCMeta, abstractmethod


class SubtitleScraper(metaclass=ABCMeta):
    """
    This is an abstract class defining a subtitle crawler and the methods to implement.
    The implementing class should scrape the subtitle files, save them on the file path and allow checking the server status.
    """
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
    def download_subtitles(self):
        pass

    @abstractmethod
    def save_subtitle_file_in_directory(self):
        pass

    @abstractmethod
    def search_subtitles_by_id(self):
        pass

