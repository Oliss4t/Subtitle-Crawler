from xmlrpc.client import ServerProxy

class OpenSubtitleCrawler:
    """
    This class defines the OpenSubtitleCrawler which accesses the opensubtitles api methods.
    The documentation of the opensubtitles api methods can be accessed at https://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC.
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
        self.__user_agent = "TemporaryUserAgent" #requested
        self.__language = "en"
        self.__login_token = ""
        self.__limit = {'limit': 5}


    def server_status(self) -> bool:
        """
        checks if the opensubtitles api endpoint is reachable. If the enpoint responds within 3 seconds the server_status is True, else False
        :return: connection result
        """
        _server_info = self.__proxy.ServerInfo()
        return True if _server_info['seconds'] <= 3.0 else False


    def login(self) -> str:
        """
        logging in into opensubtitle with the given credentials. Sets the login token, which must be used in later communication.
        :return: login result
        """
        _login_result = self.__proxy.LogIn(self.__username, self.__password, self.__language, self.__user_agent)
        if _login_result['status'] == "200 OK":
            self.__login_token = _login_result['token']
            return {"Success": "Log in successfully, and the token:" + self.__login_token}
        else:
            return {"Error": "Log in failed."}

    def logout(self) -> str:
        """
        logging out of opensubtitle.
        :return: login result
        """
        _logout_result = self.__proxy.LogOut(self.__login_token)
        if _logout_result['status'] == "200 OK":
            self.__login_token = ""
            return {"Success": "Log out successfully."}
        else:
            return {"Error": "Log out failed."}

    def search_subtitles(self, *movies) -> []:
        """
        searches opensubtitle for a list of subtitles. Returns information about found subtitles.
        :param *movies: dictionary of movies and series, containing the information movie name, season, episode
        :return: subtitle results
        """
        #TODO: look into tags, how can they be used
        for movie in movies:
            movie["sublanguageid"] = "eng"
        _search_result = self.__proxy.SearchSubtitles(self.__login_token, movies, self.__limit)
        if _search_result['status'] == "200 OK":
            _results = []
            for _r in  _search_result['data']:
                _entry = {
                    "MovieName": _r["MovieName"],
                    "MovieReleaseName": _r["MovieReleaseName"],
                    "InfoFormat": _r["InfoFormat"],
                    "SubLanguageID" : _r["SubLanguageID"],
                    "ISO639" : _r["ISO639"],
                    "MovieKind" : _r["MovieKind"],
                    "IDMovieImdb" : _r["IDMovieImdb"],
                    "IDSubtitleFile" : _r['IDSubtitleFile'],
                    "SubEncoding" : _r['SubEncoding']
                }
                _results.append(_entry)

            return {"Success": f"Found {len(_results)} entries"}, _results
        else:
            return {"Error": "Error while searching."}


    def download_subtitles(self):
        #array DownloadSubtitles( $token, array($IDSubtitleFile, $IDSubtitleFile, ...) )
        pass

    def get_cover_images(self):
        #GetIMDBMovieDetails
        pass