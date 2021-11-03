from xmlrpc.client import ServerProxy
import json

class OpenSubtitleCrawler:
    """
    This class defines the OpenSubtitleCrawler which accesses the opensubtitles api methods
    """
    def __init__(self, _username: str = "", _password: str = ""):
        """
        Constructor
        :param _username: username of the opensubtitles account
        :param _password: password of the opensubtitles account
        """
        self.__proxy = ServerProxy("http://api.opensubtitles.org/xml-rpc")
        self.__username = _username
        self.__password = _password


    def server_status(self) -> bool:
            _server_info = self.__proxy.ServerInfo()
            return True if _server_info['seconds'] <= 3.0 else False


    def login(self):
        pass

    def log_out(self):
        pass

    def search_subtitles(self):
        pass