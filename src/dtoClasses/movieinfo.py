from src.abstractClasses.media import Media
from .person import  Person


class MovieInfo(Media):
    """
    TODO
    """

    def __init__(self, name: str = "",  _id: str = "",  _year: str = "",  _image: str = "",  _genres: str = "",  _runtimes: str = "", _rating: str = "0", _votes: str = "",  _plot: str = ""
                 , _languages: str = "", _kind: str = "", _directors: [Person] = [], _writers: [Person] = [], _producers: [Person] = [], _cast: [Person] = []):
        """
        Constructor
        TODO
        """
        self.name = name
        self.id = _id
        self.year = _year
        self.image = _image
        self.genres = _genres
        self.runtimes = _runtimes
        self.rating = _rating
        self.plot = _plot
        self.votes = _votes
        self.languages = _languages
        self.kind = _kind
        self.directors = _directors
        self.writers = _writers
        self.producers = _producers
        self.cast = _cast

