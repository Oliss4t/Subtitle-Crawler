from xmlrpc.client import ServerProxy
from .abstractClasses.subtitleScraper import SubtitleScraper
from .dtoClasses.subtitle import MetaSubtitle
from .errorClasses.open_subtitle_errors import OpenSubtitleSearchError, OpenSubtitleDownloadError, OpenSubtitlSaveFilesError
import base64
import gzip
import json
from pathlib import Path

class OpenSubtitleCrawler(SubtitleScraper):
    """
    TODO
    This class defines the OpenSubtitleCrawler which accesses the opensubtitles api methods.
    The documentation of the opensubtitles api methods can be accessed at https://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC.
    """

    def __init__(self, _username: str = "", _password: str = "", _agent: str = "TemporaryUserAgent",_directory: str = "./data/downloads/"):
        """
        Constructor
        :param _username: username of the opensubtitles account
        :param _password: password of the opensubtitles account
        """
        self.__proxy = ServerProxy("http://api.opensubtitles.org/xml-rpc")
        self.__username = _username
        self.__password = _password
        self.__directory = _directory
        self.__user_agent = _agent
        self.__language = "en"
        self.__login_token = ""
        #self.__subtitle_encoding = "utf-8"
        self.__limit_single_movie = {'limit': 2}
        self.__limit_all_movies = {'limit': 50}


    def check_server_status(self) -> bool:
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


    def download_subtitles(self, _subtitles: [MetaSubtitle]):
        # LIMIT is for maximum 20 IDSubtitleFiles, others will be ignored.
        _subtitle_ids = [sub.id_subtitle_file for sub in _subtitles]
        try:
            _subtitle_result = self.__proxy.DownloadSubtitles(self.__login_token, _subtitle_ids)
            if _subtitle_result['status'] == '200 OK':
                _subtitle_data = _subtitle_result['data']
                for _subtitle in _subtitle_data:
                    self.save_subtitle_file_in_directory(_subtitle, *[_meta_subtitle for _meta_subtitle in _subtitles  if _meta_subtitle.id_subtitle_file ==_subtitle['idsubtitlefile']])
            else:
                raise OpenSubtitleDownloadError(_subtitle_result['status'])
        except OpenSubtitleDownloadError as e:
            raise e

    def save_subtitle_file_in_directory(self, _subtitle: {}, _meta_subtitle: MetaSubtitle):
        try:
            #_working_directory_str = self.__directory+'/'+_meta_subtitle.id_movie_imdb+'_'+_meta_subtitle.movie_name.replace(' ', '_')+'/'
            _working_directory_str = self.__directory + '/' + _meta_subtitle.id_movie_imdb + '/'
            _working_directory =  Path(_working_directory_str)
            _working_directory.mkdir(parents=True, exist_ok=True)
            _subtitle_path_gz = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.gz")
            _subtitle_path_txt = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.txt")
            _subtitle_path_json = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.json")
            with open(_subtitle_path_gz, 'wb') as f:
                f.write(base64.b64decode(_subtitle['data']))


            with open(_subtitle_path_json, 'w', encoding='utf-8') as f:
                json.dump(_meta_subtitle.__dict__, f, ensure_ascii=False, indent=4)

            with gzip.open(_subtitle_path_gz, 'rb') as f:
                _subfile = f.read()
                # with open(_subtitle_path_txt, "w", encoding=_meta_subtitle.sub_encoding) as f:
                #     f.write(_subfile.decode(_meta_subtitle.sub_encoding))
                with open(_subtitle_path_txt, 'w') as f:
                    f.write(_subfile.decode(_meta_subtitle.sub_encoding))
        except Exception as e:
            raise OpenSubtitlSaveFilesError(e.message if hasattr(e, 'massage') else None )


    def search_subtitles_by_id(self, _imdb_ids) -> [MetaSubtitle]:
        """
        searches opensubtitle for a list of imdb ids. Returns information about found subtitles.
        :param *movies: dictionary of movies and series, containing the information movie name, season, episode
        :return: subtitle results
        """
        _search_body = []
        for _imdb_id in _imdb_ids:
            _search_body.append({'imdbid':_imdb_id, 'sublanguageid' : "eng"})
        try:
            _subtitles = []
            # limit for each movie the subtitle files
            for _imdb_movie in _search_body:
                _search_result = self.__proxy.SearchSubtitles(self.__login_token, [_imdb_movie], self.__limit_single_movie)
                if _search_result['status'] == "200 OK":
                    for _r in _search_result['data']:
                        _subtitles.append(MetaSubtitle(_movie_name=_r["MovieName"], _movie_release_name=_r["MovieReleaseName"], _info_format=_r["InfoFormat"], _sub_language_id= _r["SubLanguageID"]
                                 ,_ISO639=_r["ISO639"], _movie_kind=_r["MovieKind"], _id_movie_imdb=_r["IDMovieImdb"], _id_subtitle_file=_r['IDSubtitleFile'], _sub_encoding=_r['SubEncoding']))
                else:
                    raise OpenSubtitleSearchError(_search_result['status'])
            return _subtitles
        except OpenSubtitleSearchError as e:
            raise e


    # def search_subtitles_by_name(self, *movies) -> []:
    #     """
    #     searches opensubtitle for a list of subtitles. Returns information about found subtitles.
    #     :param *movies: dictionary of movies and series, containing the information movie name, season, episode
    #     :return: subtitle results
    #     """
    #     #TODO: look into tags, how can they be used
    #     _movies_count_found = 0
    #     _movies_count_found = []
    #     for _movie in movies:
    #         _movie["sublanguageid"] = "eng"
    #         _matches, _results = fetch_subtitles_searches_results(_movie)
    #         _movies_count_found += _matches
    #         _movies_count_found.append()
    #
    #     print(movies)
    #     _search_result = self.__proxy.SearchSubtitles(self.__login_token, movies, self.__limit_all_movies)
    #     if _search_result['status'] == "200 OK":
    #         _results = []
    #         for _r in  _search_result['data']:
    #             _entry = {
    #                 "MovieName": _r["MovieName"],
    #                 "MovieReleaseName": _r["MovieReleaseName"],
    #                 "InfoFormat": _r["InfoFormat"],
    #                 "SubLanguageID" : _r["SubLanguageID"],
    #                 "ISO639" : _r["ISO639"],
    #                 "MovieKind" : _r["MovieKind"],
    #                 "IDMovieImdb" : _r["IDMovieImdb"],
    #                 "IDSubtitleFile" : _r['IDSubtitleFile'],
    #                 "SubEncoding" : _r['SubEncoding']
    #             }
    #             _results.append(_entry)
    #
    #         return {"Success": f"Found {len(_results)} entries"}, _results
    #     else:
    #         return {"Error": "Error while searching."}

    # def fetch_subtitles_searches_results(self, _imdb_id):
    #     _search_result = self.__proxy.SearchSubtitles(self.__login_token, _imdb_id, self.__limit_all_movies)
    #     if _search_result['status'] == "200 OK":
    #         _results = []
    #         for _r in _search_result['data']:
    #             _entry = {
    #                 "MovieName": _r["MovieName"],
    #                 "MovieReleaseName": _r["MovieReleaseName"],
    #                 "InfoFormat": _r["InfoFormat"],
    #                 "SubLanguageID": _r["SubLanguageID"],
    #                 "ISO639": _r["ISO639"],
    #                 "MovieKind": _r["MovieKind"],
    #                 "IDMovieImdb": _r["IDMovieImdb"],
    #                 "IDSubtitleFile": _r['IDSubtitleFile'],
    #                 "SubEncoding": _r['SubEncoding']
    #             }
    #             _results.append(_entry)
    #         return len(_results), _results
    #     else:
    #         return None

