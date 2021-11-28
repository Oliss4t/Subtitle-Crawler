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
    def download_subtitles(self):
        pass

    @abstractmethod
    def save_subtitle_file_in_directory(self):
        pass
        #TODO not to important
