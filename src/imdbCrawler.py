from imdb import IMDb
from .abstractClasses.mediaMetaScraper import MediaMetaScraper
from .dtoClasses.movieinfo import MovieInfo
from .dtoClasses.person import Person
from .errorClasses.open_subtitle_errors import ImdbDownloadError, ImdbSaveFilesError
from pathlib import Path
import json
import jsonpickle
import urllib.request



class ImdbCrawler(MediaMetaScraper):
    """
    TODO
    """

    def __init__(self, _directory: str = "./data/downloads/"):
        """
        Constructor
        TODO
        """
        self.__endpoint = IMDb() #create an instance of the IMDb class
        self.__directory = _directory


    def download_movie_info_by_ids(self, imdb_ids: [str]):
        try:
            _movie_infos = []
            for _imdb_id in imdb_ids:
                _movie = self.__endpoint.get_movie(_imdb_id)  # , info=['critic reviews', 'plot','release dates', 'release info','vote details','main'])
                _directors = [Person(_id = _person.getID(), _name = _person.get('name'))for _person in _movie.get('directors')]
                _writers = [Person(_id = _person.getID(), _name = _person.get('name'))for _person in _movie.get('writers')]
                _producers = [Person(_id = _person.getID(), _name = _person.get('name'))for _person in _movie.get('producers')]
                _cast = [Person(_id = _person.getID(), _name = _person.get('name'))for _person in _movie.get('cast')]

                _movie_infos.append(MovieInfo(name = _movie.get('title'), _id = _movie.get('imdbID'), _year = _movie.get('year'), _image = _movie.get_fullsizeURL()
                                              , _genres = _movie.get('genres'), _runtimes = _movie.get('runtimes'), _votes = _movie.get('votes'), _rating = _movie.get('rating')
                                              , _plot = _movie.get('plot outline'), _languages = _movie.get('languages'), _kind = _movie.get('kind'), _directors = _directors
                                              , _writers = _writers, _producers = _producers, _cast = _cast
                                              ))

            self.save_movie_infos_in_directory(_movie_infos)
        except ImdbSaveFilesError as e:
            raise e
        except Exception as e:

            raise ImdbDownloadError(e.message if hasattr(e, 'message') else None)

        #print(movie.get('genres'))
        #print(movie.get('runtimes'))
        #print(movie.get('rating'))
        #print(movie.get('votes'))
        #print(movie.get('imdbID'))
        #print(movie.get('plot outline'))
        #print(movie.get('languages'))
        #print(movie.get('title'))
        #print(movie.get('year'))
        # print(movie.get('kind'))
        # print(movie.get('directors'))
        # print(movie.get('writers'))
        # print(movie.get('producers'))
        # print(movie.get('cast'))
        #print(movie.get_fullsizeURL())

    def save_movie_infos_in_directory(self, _movie_infos: [MovieInfo]):
        try:
            for _info in _movie_infos:
                _working_directory_str = self.__directory + '/' + _info.id.strip('0') + '/'
                _working_directory = Path(_working_directory_str)
                _working_directory.mkdir(parents=True, exist_ok=True)
                _subtitle_path_json = Path(_working_directory_str, f"{_info.name}.json")
                _image_path_jpg = Path(_working_directory_str, f"{_info.name}.jpg")

                urllib.request.urlretrieve(_info.image,_image_path_jpg)

                with open(_subtitle_path_json, 'w', encoding='utf-8') as f:
                    serialized = jsonpickle.encode(_info)
                    json.dump(json.loads(serialized), f, ensure_ascii=False, indent=4)

        except Exception as e:
            raise ImdbSaveFilesError(e.message if hasattr(e, 'massage') else None)


    def get_movie_info_by_name(self):
        # movie = ia.get_movie('0133093')
        movies = self.__endpoint.search_movie('Lion King')
        for movie in movies:
            print(movie.getID())
            print(movie.get('title'))
            print(movie.get('kind'))
            print(movie.get('year'))
            print(movie.items())
            print(movie.get_fullsizeURL())

        specific_movie = self.__endpoint.get_movie('0110357')
        print(specific_movie)


    def get_series_info_by_id(self):
        series = self.__endpoint.get_movie('0389564')
        print(series)
        print(series['kind'])
        print(series.get_fullsizeURL())
        # episode = ia.get_movie('0502803')
        # print(episode)
        # print(episode['kind'])
        self.__endpoint.update(series, 'episodes')
        print(sorted(series['episodes'].keys()))
        season4 = series['episodes'][4]
        print(len(season4))
        episode = series['episodes'][4][2]
        print(episode.getID())

        print(episode['season'])
        print(episode['episode'])
        print(episode['title'])
        print(episode['series title'])
        print(episode['episode of'])
        print(series)


    def get_series_info_by_name(self):
        pass


    def get_season_info_by_id(self):
        pass


    def get_episode_info_by_id(self):
        pass





