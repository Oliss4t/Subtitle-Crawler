class MetaSubtitle:
    """
    This class defines a meta subtitle. It contains all information about a subtitle, but not the subtitle itself.
    """
    def __init__(self, _movie_name: str = "", _movie_release_name: str = "", _info_format: str = "", _sub_language_id: str = "", _ISO639: str = "", _movie_kind: str = "", _id_movie_imdb: str = "", _id_subtitle_file: str = "", _sub_encoding: str = ""):
        """
        Constructor
        :param _movie_name: movie name of the subtitle
        :param _movie_release_name: movie release name of the subtitle, incl. resolution, format, year...
        :param _info_format: info foramt: e.g. BluRay
        :param _sub_language_id: language of the subtitle
        :param _ISO639: ISO639 code of the language of the subtitle
        :param _movie_kind: movie kind: e.g movie or serie
        :param _id_movie_imdb: imdb movie id
        :param _id_subtitle_file: if of the subtitle file
        :param _sub_encoding: the encoding of the subtitle file
        """
        self.movie_name = _movie_name
        self.movie_release_name = _movie_release_name
        self.info_format = _info_format
        self.sub_language_id = _sub_language_id
        self.ISO639 = _ISO639
        self.movie_kind = _movie_kind
        self.id_movie_imdb = _id_movie_imdb
        self.id_subtitle_file = _id_subtitle_file
        self.sub_encoding = _sub_encoding

    def __eq__(self, other):
        """
        checks if MetaSubtitle object is equal to another MetaSubtitle object. Needed for Equal test.
        """
        return self.movie_name == other.movie_name and self.movie_release_name == other.movie_release_name \
               and self.info_format == other.info_format and self.sub_language_id == other.sub_language_id and self.ISO639 == other.ISO639 \
               and self.movie_kind == other.movie_kind and self.id_movie_imdb == other.id_movie_imdb and self.id_subtitle_file == other.id_subtitle_file\
               and self.sub_encoding == other.sub_encoding

