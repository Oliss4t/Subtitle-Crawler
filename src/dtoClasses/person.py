import json

class Person:
    def __init__(self, _id: str, _name: str):
        self.id = _id
        self.name = _name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)