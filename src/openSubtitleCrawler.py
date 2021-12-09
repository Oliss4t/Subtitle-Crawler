from xmlrpc.client import ServerProxy
from .abstractClasses.subtitleScraper import SubtitleScraper
from .dtoClasses.subtitle import MetaSubtitle
from .utils import CommandResponse
from .errorClasses.open_subtitle_errors import OpenSubtitleSearchError, OpenSubtitleDownloadError, \
    OpenSubtitlSaveFilesError
import base64
import gzip
import json
from pathlib import Path


class OpenSubtitleCrawler(SubtitleScraper):
    """
    This class defines the OpenSubtitleCrawler which accesses the opensubtitles api methods.
    The documentation of the open subtitles api methods can be accessed
    at https://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC.
    """

    def __init__(self, _username: str = "", _password: str = "", _agent: str = "TemporaryUserAgent",
                 _download_directory: str = "./data/downloads/", _subtitle_language: str = ""):
        """
        Constructor
        :param _username: username of the opensubtitles account
        :param _password: password of the opensubtitles account
        :param _agent: agent to use for the opensubtitles queries.
                       If none is provided the default "TemporaryUserAgent" is used. This has query limits.
        :param _download_directory: download_directory to save the files
        """
        self.__proxy = ServerProxy("http://api.opensubtitles.org/xml-rpc")
        self.__username = _username
        self.__password = _password
        self.__download_directory = _download_directory
        self.__user_agent = _agent
        self.__language = "eng"
        self.__subtitle_language = "eng" if _subtitle_language == "" else _subtitle_language
        self.__login_token = ""
        self.__limit_single_movie = {'limit': 2}
        self.__limit_all_movies = {'limit': 50}


    def check_server_status(self) -> CommandResponse:
        """
        checks if the opensubtitles api endpoint is reachable. If the enpoint responds within 3 seconds the server_status is True, else False
        :return: connection CommandResponse
        """
        _server_info = self.__proxy.ServerInfo()
        if _server_info['seconds'] <= 3.0:
            return CommandResponse(_successful=True, _message="is up and running")
        else:
            return CommandResponse(_successful=False, _message="is down")

    def login(self) -> CommandResponse:
        """
        logging in into opensubtitle with the given credentials. Sets the login token, which must be used in later communication.
        :return: login CommandResponse
        """
        try:
            _login_result = self.__proxy.LogIn(self.__username, self.__password, self.__language, self.__user_agent)
            if _login_result['status'] == "200 OK":
                self.__login_token = _login_result['token']
                return CommandResponse(_successful=True, _message="Log in successfully, and the token:" + self.__login_token)
            else:
                return CommandResponse(_successful=True, _message="Log in failed.")
        except Exception as e:
            return CommandResponse(_successful=False, _message=e.message if hasattr(e, 'message') else "Log in failed.")

    def logout(self) -> CommandResponse:
        """
        logging out of opensubtitle.
        :return: logout CommandResponse
        """
        try:
            _logout_result = self.__proxy.LogOut(self.__login_token)
            if _logout_result['status'] == "200 OK":
                self.__login_token = ""
                return CommandResponse(_successful=True, _message="Log out successfully.")
            else:
                return CommandResponse(_successful=False, _message="Log out failed.")
        except Exception as e:
            return CommandResponse(_successful=False, _message=e.message if hasattr(e, 'message') else "Log out failed.")

    def download_subtitle_from_proxy(self, _subtitle_ids):
        """
        calls the proxy to download the subtitles
        :param _subtitle_ids: list of subtitle ids
        :return: response
        """
        return self.__proxy.DownloadSubtitles(self.__login_token, _subtitle_ids)

    def download_subtitles(self, _subtitles: [MetaSubtitle]) -> CommandResponse:
        """
        downloads the subtitle files given the provided MetaSubtitle list and calls save_subtitle_file_in_directory to saves them in the download directory.
        :return: download CommandResponse
        """
        # LIMIT is for maximum 20 IDSubtitleFiles, others will be ignored.
        _subtitle_ids = [_sub.id_subtitle_file for _sub in _subtitles]
        try:
            _subtitle_result = self.download_subtitle_from_proxy(_subtitle_ids)
            if _subtitle_result['status'] == '200 OK':
                _subtitle_data = _subtitle_result['data']
                for _subtitle in _subtitle_data:
                    self.save_subtitle_file_in_directory(_subtitle, *[_meta_subtitle for _meta_subtitle in _subtitles if
                                                                      _meta_subtitle.id_subtitle_file == _subtitle['idsubtitlefile']])
                return CommandResponse(_successful=True, _message="Subtitle download successful.")
            else:
                raise OpenSubtitleDownloadError(_subtitle_result['status'])
        except OpenSubtitleDownloadError as down_e:
            print(down_e)
            return CommandResponse(_successful=False, _message=down_e.message)
        except OpenSubtitlSaveFilesError as save_e:
            print(save_e)
            return CommandResponse(_successful=False, _message=save_e.message)
        except Exception as e:
            print(e)
            return CommandResponse(_successful=False, _message=e.message if hasattr(e, 'message') else "The download failed.")

    def save_subtitle_file_in_directory(self, _subtitle: {}, _meta_subtitle: MetaSubtitle):
        """
        saves the downloaded files in the download directory.
        The following formats will be saved:
            -subtitleid.gz (encoded gz subtitle file)
            -subtitleid.txt (decoded subtitle file)
            -subtitleid.json (meta subtitle info)
        """
        try:
            _working_directory_str = self.__download_directory + '/' + _meta_subtitle.id_movie_imdb + '/'
            Path(_working_directory_str).mkdir(parents=True, exist_ok=True)
            _subtitle_path_gz = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.gz")
            _subtitle_path_txt = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.txt")
            _subtitle_path_json = Path(_working_directory_str, f"{_subtitle['idsubtitlefile']}.json")

            self.save_gz_format_in_directory(_subtitle['data'], _subtitle_path_gz)
            self.save_json_format_in_directory(_meta_subtitle, _subtitle_path_json)
            self.save_txt_format_in_directory(_meta_subtitle, _subtitle_path_gz, _subtitle_path_txt)

        except Exception as e:
            print(e)
            raise OpenSubtitlSaveFilesError(e.message if hasattr(e, 'message') else None)

    def save_gz_format_in_directory(self, _subtitle, _directory_path):
        """
        saves the file subtitleid.gz (encoded gz subtitle file) in the download directory.)
        """
        with open(_directory_path, 'wb') as f:
            f.write(base64.b64decode(_subtitle))

    def save_json_format_in_directory(self, _meta_subtitle, _directory_path):
        """
        saves the file subtitleid.json (meta subtitle info) in the download directory.
        """
        with open(_directory_path, 'w', encoding='utf-8') as f:
            json.dump(_meta_subtitle.__dict__, f, ensure_ascii=False, indent=4)

    def save_txt_format_in_directory(self, _meta_subtitle, _directory_read_path, _directory_save_path):
        """
        saves the file subtitleid.txt (decoded subtitle file) in the download directory.
        """
        with gzip.open(_directory_read_path, 'rb') as f:
            _subfile = f.read()
            with open(_directory_save_path, 'w') as ff:
                ff.write(_subfile.decode(_meta_subtitle.sub_encoding))

    def search_subtitle_from_proxy(self, _imdb_movie):
        """
        calls the proxy to fetch the subtitle meta
        :param _imdb_movie: imdb id
        :return: response
        """
        return self.__proxy.SearchSubtitles(self.__login_token, [_imdb_movie], self.__limit_single_movie)

    def search_subtitles_by_id(self, _imdb_ids: [str]) -> [MetaSubtitle]:
        """
        searches opensubtitle for a list of imdb ids. Returns information about found subtitles.
        :param _imdb_ids: list of imdb ids
        :return: list of MetaSubtitles
        """
        _search_body = []
        for _imdb_id in _imdb_ids:
            _search_body.append({'imdbid': _imdb_id, 'sublanguageid': self.__subtitle_language})
        try:
            _subtitles = []
            # limit for each movie the subtitle files
            for _imdb_movie in _search_body:
                _search_result = self.search_subtitle_from_proxy(_imdb_movie)
                if _search_result['status'] == "200 OK":
                    for _r in _search_result['data']:
                        _subtitles.append(
                            MetaSubtitle(_movie_name=_r["MovieName"], _movie_release_name=_r["MovieReleaseName"],
                                         _info_format=_r["InfoFormat"], _sub_language_id=_r["SubLanguageID"]
                                         , _ISO639=_r["ISO639"], _movie_kind=_r["MovieKind"],
                                         _id_movie_imdb=_r["IDMovieImdb"], _id_subtitle_file=_r['IDSubtitleFile'],
                                         _sub_encoding=_r['SubEncoding']))
                else:
                    raise OpenSubtitleSearchError(_search_result['status'])
            return _subtitles
        except OpenSubtitleSearchError as e:
            raise e

    ## TODO: look into tags, how can they be used
    # def search_subtitles_by_name(self, *movies) -> []:
    #     """
    #     searches opensubtitle for a list of subtitles. Returns information about found subtitles.
    #     :param *movies: dictionary of movies and series, containing the information movie name, season, episode
    #     :return: subtitle results
    #     """
    #
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
