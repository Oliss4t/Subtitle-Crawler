from .person import Person


class MovieInfo:
    """
    This class defines a movie information from IMDB. It contains all additional information about a movie.
    e.g. the image url.
    """
    def __init__(self, name: str = "",  _id: str = "",  _year: str = "",  _image_url: str = "",  _genres: str = "",  _runtimes: str = "", _rating: str = "0", _votes: str = "",  _plot: str = ""
                 , _languages: str = "", _kind: str = "", _directors: [] = [], _writers: [] = [], _producers: [] = [], _cast: [] = []):
        """
        Constructor
        :param name: name of the movie
        :param _id: imdb id of the movie
        :param _year: year of the movie release
        :param _image_url: image url of the movie still
        :param _genres: genres of the movie
        :param _runtimes: runtime of the movie
        :param _rating: rating of the movie
        :param _plot: plot of the movie
        :param _votes: imdb votes of the movie
        :param _kind: kind of the movie
        :param _directors: directors of the of the movie
        :param _writers: writers of the of the movie
        :param _producers: producers of the of the movie
        :param _cast: cast of the of the movie
        """
        self.name = name
        self.id = _id
        self.year = _year
        self.image_url = _image_url
        self.genres = _genres
        self.runtimes = _runtimes
        self.rating = _rating
        self.plot = _plot
        self.votes = _votes
        self.languages = _languages
        self.kind = _kind
        self.directors = [Person(_id=_person.getID(), _name=_person.get('name')) for _person in _directors]
        self.writers = [Person(_id=_person.getID(), _name=_person.get('name')) for _person in _writers]
        self.producers = [Person(_id=_person.getID(), _name=_person.get('name')) for _person in _producers]
        self.cast = [Person(_id=_person.getID(), _name=_person.get('name')) for _person in _cast]
        self.directors = _directors
        self.writers = _writers
        self.producers = _producers
        self.cast = _cast

