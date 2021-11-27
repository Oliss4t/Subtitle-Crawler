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
        self.__limit_single_movie = {'limit': 5}
        self.__limit_all_movies = {'limit': 50}


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
        _movies_count_found = 0
        _movies_count_found = []
        for _movie in movies:
            _movie["sublanguageid"] = "eng"
            _matches, _results = fetch_subtitles_searches_results(_movie)
            _movies_count_found += _matches
            _movies_count_found.append()

        print(movies)
        _search_result = self.__proxy.SearchSubtitles(self.__login_token, movies, self.__limit_all_movies)
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

    def fetch_subtitles_searches_results(self, movie):
        _search_result = self.__proxy.SearchSubtitles(self.__login_token, movie, self.__limit_all_movies)
        if _search_result['status'] == "200 OK":
            _results = []
            for _r in _search_result['data']:
                _entry = {
                    "MovieName": _r["MovieName"],
                    "MovieReleaseName": _r["MovieReleaseName"],
                    "InfoFormat": _r["InfoFormat"],
                    "SubLanguageID": _r["SubLanguageID"],
                    "ISO639": _r["ISO639"],
                    "MovieKind": _r["MovieKind"],
                    "IDMovieImdb": _r["IDMovieImdb"],
                    "IDSubtitleFile": _r['IDSubtitleFile'],
                    "SubEncoding": _r['SubEncoding']
                }
                _results.append(_entry)
            return len(_results), _results
        else:
            return None


    def download_subtitles(self):
        #array DownloadSubtitles( $token, array($IDSubtitleFile, $IDSubtitleFile, ...) )
        #def download_subtitles(self, movie_name, subtitleID, encoding):
        #LIMIT is for maximum 20 IDSubtitleFiles, others will be ignored.
        q = []
        q.append(subtitleID)

        content = self.proxy.DownloadSubtitles(self.token, q)
        if content['status'] == '200 OK':
            # print(content)
            data_array = content['data']
            data = data_array[0]['data']
            with open(movie_name + ".gz", 'wb') as f:
                f.write(base64.b64decode(data))

            with gzip.open(movie_name + ".gz", 'rb') as f:
                s = f.read()

            with open(movie_name, 'w') as f:
                f.write(s.decode(encoding))
        pass

    def get_cover_images(self):
        #GetIMDBMovieDetails
        pass