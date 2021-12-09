from imdb import IMDb
from .abstractClasses.mediaMetaScraper import MediaMetaScraper
from .dtoClasses.movieinfo import MovieInfo
from .dtoClasses.person import Person
from .utils import CommandResponse
from .errorClasses.open_subtitle_errors import ImdbDownloadError, ImdbSaveInfoError, ImdbSaveImageError
from pathlib import Path
import json
import jsonpickle
import urllib.request



class ImdbCrawler(MediaMetaScraper):
    """
    This class defines the Imdb Crawler which accesses the Imdb api methods.
    The documentation of the Imdb api methods can be accessed
    at https://imdbpy.readthedocs.io/en/latest/.
    """

    def __init__(self, _download_directory: str = "./data/downloads/"):
        """
        Constructor
        :param _download_directory: download_directory to save the files
        """
        self.__endpoint = IMDb()
        self.__download_directory = _download_directory


    def download_movie_info_by_ids(self, imdb_ids: [str]) -> CommandResponse:
        """
        downloads the imdb information for all provided imdb ids
        and calls save_movie_infos_in_directory to save them in the download directory.
        :return: download CommandResponse
        """
        try:
            _movie_infos = []
            for _imdb_id in imdb_ids:
                _movie = self.__endpoint.get_movie(_imdb_id)
                _movie_infos.append(MovieInfo(name = _movie.get('title'), _id = _movie.get('imdbID'), _year = _movie.get('year'), _image_url = _movie.get_fullsizeURL()
                                              , _genres = _movie.get('genres'), _runtimes = _movie.get('runtimes'), _votes = _movie.get('votes'), _rating = _movie.get('rating')
                                              , _plot = _movie.get('plot outline'), _languages = _movie.get('languages'), _kind = _movie.get('kind'), _directors = _movie.get('directors')
                                              , _writers = _movie.get('writers'), _producers = _movie.get('producers'), _cast = _movie.get('cast')
                                              ))

            self.save_movie_infos_in_directory(_movie_infos)
            return CommandResponse(_successful=True, _message='Movie information and image download successful.')

        except ImdbSaveInfoError as _info_e:
            return CommandResponse(_successful=False, _message=_info_e.message)
        except ImdbSaveImageError as _image_e:
            return CommandResponse(_successful=False, _message=_image_e.message)
        except Exception as e:
            print(e)
            return CommandResponse(_successful=False, _message=ImdbDownloadError(e.message if hasattr(e, 'message') else None).message)



    def save_movie_infos_in_directory(self, _movie_infos: [MovieInfo]):
        """
        saves the downloaded imdb information in the download directory
        and calls save_movie_image_in_directory to save the image in the download directory.
        The following formats will be saved:
            -moviename.json (meta subtitle info)
        """
        try:
            for _info in _movie_infos:
                _working_directory_str = self.__download_directory + '/' + _info.id.strip('0') + '/'
                Path(_working_directory_str).mkdir(parents=True, exist_ok=True)
                _subtitle_path_json = Path(_working_directory_str, f"{_info.name}.json")
                _image_path_jpg = Path(_working_directory_str, f"{_info.name}.jpg")

                self.save_movie_image_in_directory(_info.image_url, _image_path_jpg)

                with open(_subtitle_path_json, 'w', encoding='utf-8') as f:
                    serialized = jsonpickle.encode(_info)
                    json.dump(json.loads(serialized), f, ensure_ascii=False, indent=4)

        except ImdbSaveImageError as _image_e:
            raise _image_e
        except Exception as e:
            raise ImdbSaveInfoError(e.message if hasattr(e, 'massage') else None)


    def save_movie_image_in_directory(self,_image_url: str, _image_path_jpg: Path):
        """
        downloads imdb image and saves it in the download directory
        The following formats will be saved:
            -moviename.jpg (movie image)
        """
        try:
            urllib.request.urlretrieve(_image_url, _image_path_jpg)
        except Exception as e:
            raise ImdbSaveImageError(e.message if hasattr(e, 'massage') else None)


    def get_series_info_by_id(self):
        pass
    # def get_series_info_by_id(self):
    #     series = self.__endpoint.get_movie('0389564')
    #     print(series)
    #     print(series['kind'])
    #     print(series.get_fullsizeURL())
    #     # episode = ia.get_movie('0502803')
    #     # print(episode)
    #     # print(episode['kind'])
    #     self.__endpoint.update(series, 'episodes')
    #     print(sorted(series['episodes'].keys()))
    #     season4 = series['episodes'][4]
    #     print(len(season4))
    #     episode = series['episodes'][4][2]
    #     print(episode.getID())
    #
    #     print(episode['season'])
    #     print(episode['episode'])
    #     print(episode['title'])
    #     print(episode['series title'])
    #     print(episode['episode of'])
    #     print(series)







