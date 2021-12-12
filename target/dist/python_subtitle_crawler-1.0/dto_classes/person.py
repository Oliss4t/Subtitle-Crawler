import json

class Person:
    """
    This class defines a Person occurring in a movie.
    """
    def __init__(self, _id: str, _name: str):
        """
        Constructor
        :param _id: imdb id of the person
        :param _name: name of the person
        """
        self.id = _id
        self.name = _name

    def toJSON(self):
        """
        to dump the person class to a json file
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)